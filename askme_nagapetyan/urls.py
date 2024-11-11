"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.get_main_page, name='main'),
    path('login/', views.get_login_page, name='login'),
    path('settings/', views.get_settings_page, name='settings'),
    path('signup/', views.get_signup_page, name='signup'),
    path('ask/', views.get_ask_question_page, name='ask'),
    path('question/<int:question_id>', views.get_question_page, name='question'),
    path('tag/<int:tag_id>/', views.get_tag_page, name='tag'),
    path('hot/', views.get_hot_page, name='hot'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
