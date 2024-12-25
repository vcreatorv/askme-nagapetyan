import jwt
import time
from cent import Client, PublishRequest

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.forms.models import model_to_dict
from django.core.cache import cache

from .forms import LoginForm, SignupForm, ProfileForm, AskForm, AnswerForm
from .models import Question, Tag, Profile, Answer, QuestionLike, AnswerLike
from .utils import paginate_objects

from django.conf import settings as conf_settings


client = Client(conf_settings.CENTRIFUGO_API_URL, conf_settings.CENTRIFUGO_API_KEY, timeout=1)


def get_centrifugo_data(user_id, channel):
     return {
        'centrifugo': {
            'token': jwt.encode(
                {"sub": str(user_id), "exp": int(time.time()) + 10 * 60}, 
                conf_settings.CENTRIFUGO_TOKEN_HMAC_SECRET_KEY, 
                algorithm="HS256",
            ),
            'ws_url': conf_settings.CENTRIFUGO_WS_URL,
            'channel': channel,
        }
    }

def get_popular_tags():
    cache_key = "popular_tags"
    tags = cache.get(cache_key)
    
    # Без использования cron
    # if not tags: 
    #     tags = Tag.objects.popular()
    #     cache.set(cache_key, tags, 10)

    return tags

def get_top_users():
    cache_key = "top_users"
    users = cache.get(cache_key)

    # Без использования cron
    # if not users:
    #     users = Profile.objects.get_top_users()
    #     cache.set(cache_key, users, 10)
    
    return users


def get_base_context():
    return {
        'tags': get_popular_tags(),
        'top_user_profiles': get_top_users(),
    }


def get_index_page(request):
    questions = Question.objects.new()

    if request.user.is_authenticated:
        questions = questions.annotate(
            is_liked=Exists(
                QuestionLike.objects.filter(user=request.user, question=OuterRef('pk'))
            )
        )

    page_obj = paginate_objects(request, questions)
    context = get_base_context()
    context['page_obj'] = page_obj
    return render(request, 'index.html', context)


def get_hot_questions_page(request):
    questions = Question.objects.hot()
    page_obj = paginate_objects(request, questions)
    context = get_base_context()
    context['page_obj'] = page_obj
    return render(request, 'hot.html', context)


def get_login_page(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next') or request.GET.get('continue', 'index'))

    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(request.GET.get('next') or request.GET.get('continue', 'index'))
            login_form.add_error(None, 'Incorrect username or password')
    context = get_base_context()
    context['form'] = login_form
    return render(request, 'login.html', context)


@login_required(login_url="/login/")
def get_settings_page(request):
    profile_form = ProfileForm(instance=request.user.profile, user=request.user)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile, user=request.user)
        if profile_form.is_valid():
            profile_form.save()
            auth.login(request, request.user)
            return redirect('settings')
    context = get_base_context()
    context['form'] = profile_form
    return render(request, 'settings.html', context)


@login_required(login_url="/login/")
def logout(request):
    auth.logout(request)
    return redirect('index')


def get_signup_page(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next') or request.GET.get('continue', 'index'))

    signup_form = SignupForm()
    if request.method == 'POST':
        signup_form = SignupForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = signup_form.save()
            if user:
                auth.login(request, user)
                return redirect('index')
    context = get_base_context()
    context['form'] = signup_form
    return render(request, 'signup.html', context)


@login_required(login_url="/login/")
def get_ask_question_page(request):
    ask_form = AskForm(user=request.user)
    if request.method == 'POST':
        ask_form = AskForm(request.POST, user=request.user)
        if ask_form.is_valid():
            question = ask_form.save()
            return redirect('question', question_id=question.pk)
    context = get_base_context()
    context['form'] = ask_form
    return render(request, 'ask.html', context)


def get_question_page(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    is_liked = False
    answers = Answer.objects.get_answers(question_id)
    if request.user.is_authenticated:
        is_liked = QuestionLike.objects.filter(user=request.user, question=question).exists()
        answers = answers.annotate(
            is_liked=Exists(
                AnswerLike.objects.filter(user=request.user, answer=OuterRef('pk'))
            )
        )

    page_obj = paginate_objects(request, answers)

    answer_form = AnswerForm(question_id=question_id, user=request.user)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        answer_form = AnswerForm(request.POST, question_id=question_id, user=request.user)
        if answer_form.is_valid():
            answer = answer_form.save()
            
            answer_data = model_to_dict(answer)
            answer_data['author'] = {
                'id': answer.author.id,
                'username': answer.author.username,
                'profile': {
                    'avatar': {
                        'url': answer.author.profile.avatar.url
                    }
                }
            }
            publish_request = PublishRequest(channel=f'question.{question_id}', data=answer_data)
            client.publish(publish_request)

            return redirect(reverse('question', args=[question_id]) + f'#answer-{answer.pk}')
    
    context = get_base_context()
    context['question'] = question
    context['is_liked'] = is_liked
    context['page_obj'] = page_obj
    context['form'] = answer_form
    context['centrifugo'] = get_centrifugo_data(request.user.id, f'question.{question_id}')['centrifugo']
    print(context['centrifugo'])

    return render(request, 'question.html', context)


def get_tag_questions_page(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    questions = Question.objects.tagged(tag.name)

    if request.user.is_authenticated:
        questions = questions.annotate(
            is_liked=Exists(
                QuestionLike.objects.filter(user=request.user, question=OuterRef('pk'))
            )
        )

    page_obj = paginate_objects(request, questions)
    context = get_base_context()
    context['page_obj'] = page_obj
    context['tag'] = tag
    return render(request, 'tag.html', context)


@require_POST
def question_like(request, question_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    question = get_object_or_404(Question, pk=question_id)
    like, like_created = QuestionLike.objects.get_or_create(user=request.user, question=question)

    liked = True
    if not like_created:
        like.delete()
        liked = False

    question.save()
    return JsonResponse(
        {'question_likes_count': QuestionLike.objects.filter(question=question).count(), 'liked': liked})


@require_POST
def answer_like(request, answer_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    answer = get_object_or_404(Answer, pk=answer_id)
    like, like_created = AnswerLike.objects.get_or_create(user=request.user, answer=answer)

    liked = True
    if not like_created:
        like.delete()
        liked = False

    answer.save()
    return JsonResponse({'answer_likes_count': AnswerLike.objects.filter(answer=answer).count(), 'liked': liked})



@require_POST
def helpful_answer(request, answer_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    answer = get_object_or_404(Answer, pk=answer_id)
    if answer.question.author != request.user:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    if answer.helpful:
        answer.helpful = False
    else:
        answer.helpful = True

    answer.save()

    return JsonResponse({'helpful': answer.helpful}, status=200)
