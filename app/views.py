from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, get_object_or_404

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
    return render(request, 'login.html', get_base_context())


def get_settings_page(request):
    context = get_base_context()
    context['auth_user'] = SINGLETON_USER
    return render(request, 'settings.html', context)


def get_signup_page(request):
    return render(request, 'signup.html', get_base_context())


def get_ask_question_page(request):
    return render(request, 'ask.html', get_base_context())


def get_question_page(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = Answer.objects.get_answers(question_id)
    page_obj = paginate_objects(request, answers)
    context = get_base_context()
    context['question'] = question
    context['page_obj'] = page_obj
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
