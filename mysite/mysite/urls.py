"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
# Built in authentication views from Django
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    # Calling for built in views for authentication made by django
    # Important: Django by default looks for the login.html from a specific file path - registration/login.html
    # If you want to change the default you have to specify it as an argument after as_view('file/path') Otherwise it defaults to the
    # URL specified in settings.py: LOGIN_REDIRECT_URL
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # Redirects after logging out to URL specified in settings.py: LOGOUT_REDIRECT_URL
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout')
]
