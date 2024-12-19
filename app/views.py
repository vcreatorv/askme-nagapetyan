from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import LoginForm, SignupForm, ProfileForm, AskForm, AnswerForm
from .models import Question, Tag, Profile, Answer, QuestionLike
from .utils import paginate_objects


def get_base_context():
    return {
        'tags': Tag.objects.popular(),
        'top_user_profiles': Profile.objects.get_top_users(),
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

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(request.GET.get('next') or request.GET.get('continue', 'index'))
            login_form.add_error(None, 'Incorrect username or password')
    context = get_base_context()
    context['form'] = LoginForm()
    return render(request, 'login.html', context)


@login_required(login_url="/login/")
def get_settings_page(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile, user=request.user)
        if profile_form.is_valid():
            profile_form.save()
            auth.login(request, request.user)
            return redirect('settings')
    context = get_base_context()
    context['form'] = ProfileForm(instance=request.user.profile, user=request.user)
    return render(request, 'settings.html', context)


@login_required(login_url="/login/")
def logout(request):
    auth.logout(request)
    return redirect('index')


def get_signup_page(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next') or request.GET.get('continue', 'index'))

    if request.method == 'POST':
        signup_form = SignupForm(request.POST, request.FILES)
        if signup_form.is_valid():
            user = signup_form.save()
            if user:
                auth.login(request, user)
                return redirect('index')
    context = get_base_context()
    context['form'] = SignupForm()
    return render(request, 'signup.html', context)


@login_required(login_url="/login/")
def get_ask_question_page(request):
    if request.method == 'POST':
        ask_form = AskForm(request.POST, user=request.user)
        if ask_form.is_valid():
            question = ask_form.save()
            return redirect('question', question_id=question.pk)
    context = get_base_context()
    context['form'] = AskForm(user=request.user)
    return render(request, 'ask.html', context)


def get_question_page(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = Answer.objects.get_answers(question_id)
    page_obj = paginate_objects(request, answers)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        answer_form = AnswerForm(request.POST, question_id=question_id, user=request.user)
        if answer_form.is_valid():
            answer = answer_form.save()
            return redirect(reverse('question', args=[question_id]) + f'#answer-{answer.pk}')
    context = get_base_context()
    context['question'] = question
    context['page_obj'] = page_obj
    context['form'] = AnswerForm(question_id=question_id, user=request.user)
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
