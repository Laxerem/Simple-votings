from django.contrib import admin
from django.urls import path
from django_site.views import register, home, user_login, main, profile

urlpatterns = [
    path("", main, name="main"),
    path('register', register, name="register"),
    path('login', user_login, name="login"),
    path('home', home, name="home"),
    path('profile', profile, name="profile")
]