from django.contrib import admin
from django.urls import path
from django_site.views import register, home, user_login, main, profile, user_logout, delete_user, create_survey, add_choices, create_poll, vote_list

urlpatterns = [
    path("", main, name="main"),
    path('register', register, name="register"),
    path('login', user_login, name="login"),
    path('home', home, name="home"),
    path('profile', profile, name="profile"),
    path('logout/', user_logout, name="logout"),
    path('delete/user/', delete_user, name="profile_delete"),
    path('create_voting/', create_survey, name="create_votings"),
    path('create_voting/<int:survey_id>/', create_poll, name="create_poll"),
    path('vote_list/', vote_list, name="vote_list"),
]