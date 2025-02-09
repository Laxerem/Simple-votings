from django.contrib import admin
from django.urls import path
from django_site.views import register, home

urlpatterns = [
    path('register', register, name="register"),
    path('home', home, name="home")
]