from django.shortcuts import render


tags = [
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

question = {
        "id": 3,
        "title": "How to use FileReader in JavaScript?",
        "description": "I need to read file contents with FileReader in JavaScript.",
        "user": {
            "id": 103,
            "avatar": f'/uploads/1.jpg',
            "reputation": 8
        },
        "tags": [
            {"id": 2, "name": "JavaScript"},
            {"id": 9, "name": "File API"}
        ],
        "answers": [
            {   
                "id": 1,
                "created_at": "2024-10-04T14:15:00Z",
                "user": {
                    "id": 103,
                    "avatar": f'/uploads/1.jpg',
                    "reputation": 113
                },
                "content": "One of the most popular FileReader methods is readAsDataURL. It allows you to read a file and convert it to a string that can be used as a source for img elements. This is especially useful for previewing images before uploading them to the server. Here is a sample code that shows how to do this. In this example, we create a FileReader object, add an onload event handler that will be called after the file is read, and call the readAsDataURL method to read the file.",
            },
            {   
                "id": 2,
                "created_at": "2024-10-05T18:10:00Z",
                "user": {
                    "id": 10,
                    "avatar": f'/uploads/1.jpg',
                    "reputation": 67
                },
                "content": "To use FileReader in JavaScript, you need to create a FileReader object and use its methods to read the contents of the file. FileReader provides several methods for reading files in various formats, such as readAsDataURL, readAsText, readAsArrayBuffer and readAsBinaryString. The most commonly used method is readAsDataURL, which allows you to read a file and convert it to a string that can be used as a source for img elements. Here is a sample code that shows how to do this:",
            }  
        ]  
}


def get_questions_list():
    new_questions = []
    for i in range(1, 30):
        question_data = {
            'id': i,
            'title': f'Card title {i}',
            'text': f'Some quick example text to build on the card title and make up the bulk of the card\'s content. {i}',
            'answer': i,
            'tags': [
                {"id": 1, "name": "Python"},
                {"id": 2, "name": "Django"},
                {"id": 3, "name": "MongoDB"},
                {"id": 4, "name": "Web"}
            ],
            'user': {
                'id': 1,
                'avatar': f'/uploads/1.jpg',
                'reputation': i % 5 + 1,
            },
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


def get_login_page(request):
    context = {
        'tags': tags,
        'top_users': top_users,
    }
    return render(request, 'login.html', context)

def get_settings_page(request):
    context = {
        'auth_user': auth_user,
        'tags': tags,
        'top_users': top_users,
    }
    return render(request, 'settings.html', context)


def get_signup_page(request):
    context = {
        'tags': tags,
        'top_users': top_users,
    }
    return render(request, 'signup.html', context)

def get_ask_question_page(request):
    context = {
        'tags': tags,
        'top_users': top_users,
    }
    return render(request, 'ask.html', context)


def get_question_page(request):
    context = {
        "question": question,
        'tags': tags,
        'top_users': top_users,
    }
    return render(request, 'question.html', context)
