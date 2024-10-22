from django.shortcuts import render


tags = [
    {"id": 1, "name": "Python"},
    {"id": 2, "name": "Django"},
    {"id": 3, "name": "MongoDB"},
    {"id": 4, "name": "Web"},
    {"id": 5, "name": "Java"},
    {"id": 6, "name": "Algorithms"},
    {"id": 7, "name": "VS Code"},
    {"id": 8, "name": "PostgreSQL"},
]

top_users = [
    {"id": 1, "username": "DeOwl"},
    {"id": 2, "username": "LeoY"},
    {"id": 3, "username": "Arts"},
    {"id": 4, "username": "Tractor"},
    {"id": 5, "username": "ImperialMelon"},
]

auth_user = {
    "id": 1,
    "username": "Valery Nagapetyan",
    'avatar': f'/uploads/1.jpg',
}

def get_questions_list():
    new_questions = []
    for i in range(1, 30):
        question_data = {
            'id': i,
            'title': f'Card title {i}',
            'text': f'Some quick example text to build on the card title and make up the bulk of the card\'s content. {i}',
            'answer': i,
            'tags': [f'Tag {i}-1', f'Tag {i}-2', f'Tag {i}-3', f'Tag {i}-4'],
            'avatar': f'/uploads/1.jpg',
            'reputation': i % 5 + 1,
        }
        new_questions.append(question_data)
    return new_questions


def get_new_questions_page(request):
    context = {
        'auth_user': auth_user,
        'new_questions': get_questions_list(),
        'tags': tags,
        'top_users': top_users,
    }
    return render(request, 'index.html', context)