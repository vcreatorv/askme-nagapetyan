from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_index_page, name='index'),
    path('login/', views.get_login_page, name='login'),
    path('profile/edit/', views.get_settings_page, name='settings'),
    path('signup/', views.get_signup_page, name='signup'),
    path('ask/', views.get_ask_question_page, name='ask'),
    path('question/<int:question_id>', views.get_question_page, name='question'),
    path('tag/<int:tag_id>/', views.get_tag_questions_page, name='tag'),
    path('hot/', views.get_hot_questions_page, name='hot'),
]
