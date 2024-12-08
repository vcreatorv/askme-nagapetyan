from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import LoginForm, SignupForm, ProfileForm, AskForm, AnswerForm
from .models import Question, Tag, Profile, Answer
from .utils import paginate_objects

SINGLETON_USER = User(id=1, username="admin")


def get_base_context():
    return {
        'tags': Tag.objects.popular(),
        'top_user_profiles': Profile.objects.get_top_users(),
    }


def get_index_page(request):
    questions = Question.objects.new()
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
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(request.GET.get("continue", "index"))
            login_form.add_error(None, 'Incorrect username or password')
    context = get_base_context()
    context['form'] = login_form
    return render(request, 'login.html', context)


@login_required
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


@login_required
def logout(request):
    auth.logout(request)
    return redirect('index')


def get_signup_page(request):
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


@login_required
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
    answers = Answer.objects.get_answers(question_id)
    page_obj = paginate_objects(request, answers)

    answer_form = AnswerForm(question_id=question_id, user=request.user)
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
    context['form'] = answer_form
    return render(request, 'question.html', context)


def get_tag_questions_page(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    questions = Question.objects.tagged(tag.name)
    page_obj = paginate_objects(request, questions)
    context = get_base_context()
    context['page_obj'] = page_obj
    context['tag'] = tag
    context['auth_user'] = SINGLETON_USER
    return render(request, 'tag.html', context)
