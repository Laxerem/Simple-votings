from django.contrib import admin
from django.urls import path
from django_site.views import register, home, user_login, main, profile, user_logout, delete_user, create_poll, add_choices

urlpatterns = [
    path("", main, name="main"),
    path('register', register, name="register"),
    path('login', user_login, name="login"),
    path('home', home, name="home"),
    path('profile', profile, name="profile"),
    path('logout/', user_logout, name="logout"),
    path('delete/user/', delete_user, name="profile_delete"),
    path('create_voting/', create_poll, name="create_votings"),
    path('add_choices/<int:poll_id>/', add_choices, name="add_choices"),
]