from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

TAGS = [
    {"id": 1, "name": "Python"},
    {"id": 2, "name": "Django"},
    {"id": 3, "name": "MongoDB"},
    {"id": 4, "name": "Web"},
    {"id": 5, "name": "JavaScript"},
    {"id": 6, "name": "Algorithms"},
    {"id": 7, "name": "VS Code"},
    {"id": 8, "name": "PostgreSQL"},
    {"id": 9, "name": "File API"},
]

USERS = [{
    "id": i,
    "username": f'User {i}',
    'avatar': f'/uploads/1.jpg',
    'reputation': i,
} for i in range(1, 100)
]

ANSWERS = [{
    "id": i,
    "question_id": i,
    "created_at": "2024-10-04T14:15:00Z",
    'user': USERS[i % (len(USERS) - 1)],
    "content": "One of the most popular FileReader methods is readAsDataURL. It allows you to read a file and convert it to a string that can be used as a source for img elements. This is especially useful for previewing images before uploading them to the server. Here is a sample code that shows how to do this. In this example, we create a FileReader object, add an onload event handler that will be called after the file is read, and call the readAsDataURL method to read the file.",
} for i in range(1, 100)
]

QUESTIONS = [{
    'id': i,
    'title': f'Card title {i}',
    'description': f'Some quick example text to build on the card title and make up the bulk of the card\'s content. {i}',
    'tags': TAGS[0:(i) % (len(TAGS) + 1)],
    'answer': sum(1 for a in ANSWERS if a['question_id'] == i),
    'user': USERS[i % (len(USERS) - 1)]
} for i in range(1, 100)
]


def get_top_users():
    return sorted(USERS, key=lambda x: x['reputation'], reverse=True)[:5]


def get_base_context():
    return {
        'tags': TAGS,
        'top_users': get_top_users(),
    }


def paginate_objects(request, objects, per_page=5):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page', 1)
    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(1)
    return paginated_objects


def get_main_page(request):
    context = get_base_context()
    context['page_obj'] = paginate_objects(request, QUESTIONS)
    return render(request, 'index.html', context)


def get_hot_page(request):
    context = get_base_context()
    context['page_obj'] = paginate_objects(request, QUESTIONS)
    return render(request, 'hot.html', context)


def get_login_page(request):
    context = get_base_context()
    return render(request, 'login.html', context)


def get_settings_page(request):
    context = get_base_context()
    context['auth_user'] = USERS[0]
    return render(request, 'settings.html', context)


def get_signup_page(request):
    return render(request, 'signup.html', get_base_context())


def get_ask_question_page(request):
    return render(request, 'ask.html', get_base_context())


def get_question_page(request, question_id=3):
    context = get_base_context()
    question = next((q for q in QUESTIONS if q['id'] == question_id), None)
    if not question:
        raise Http404("Question not found")

    question_answers = [a for a in ANSWERS if a['question_id'] == question_id]
    question['answers'] = question_answers

    context['question'] = question
    context['page_obj'] = paginate_objects(request, question_answers)
    return render(request, 'question.html', context)


def get_tag_question_list(chosen_tag):
    if not chosen_tag:
        return None
    tag_name = chosen_tag['name']
    return [q for q in QUESTIONS if any(tag['id'] == chosen_tag['id'] for tag in q['tags'])]


def get_tag_page(request, tag_id=1):
    tag = next((t for t in TAGS if t['id'] == tag_id), None)
    if not tag:
        raise Http404("Tag not found")

    context = get_base_context()
    context['auth_user'] = USERS[0]
    context['tag'] = tag
    context['page_obj'] = paginate_objects(request, get_tag_question_list(tag))
    return render(request, 'tag.html', context)
