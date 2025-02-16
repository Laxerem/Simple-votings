from django.contrib import admin
from django.urls import path
from django_site.views import register, home, login, main

urlpatterns = [
    path("", main, name="main"),
    path('register', register, name="register"),
    path('login', login, name="login"),
    path('home', home, name="home")
]