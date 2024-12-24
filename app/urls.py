from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_index_page, name='index'),
    path('login/', views.get_login_page, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/edit/', views.get_settings_page, name='settings'),
    path('signup/', views.get_signup_page, name='signup'),
    path('ask/', views.get_ask_question_page, name='ask'),
    path('question/<int:question_id>', views.get_question_page, name='question'),
    path('tag/<int:tag_id>/', views.get_tag_questions_page, name='tag'),
    path('hot/', views.get_hot_questions_page, name='hot'),
    path('question_like/<int:question_id>/', views.question_like, name='question_like'),
    path('answer_like/<int:answer_id>/', views.answer_like, name='answer_like'),
    path('helpful_answer/<int:answer_id>/', views.helpful_answer, name='helpful_answer')
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

