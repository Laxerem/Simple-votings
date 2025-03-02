from django.contrib import admin
from django.urls import path

from django_site.views import register, delete_choice, results, vote, edit_profile, home, user_login, main, profile, user_logout, delete_user, create_survey, add_choices, survey_editor, vote_list

urlpatterns = [
    path("admin", admin.site.urls, name="admin"),
    path("", main, name="main"),
    path('register', register, name="register"),
    path('login', user_login, name="login"),
    path('home', home, name="home"),
    path('profile', profile, name="profile"),
    path('logout/', user_logout, name="logout"),
    path('delete/user/', delete_user, name="profile_delete"),
    path('user/edit_profile', edit_profile, name="edit_profile"),
    path('create_voting/', create_survey, name="create_votings"),
    path('create_voting/<int:survey_id>/', survey_editor, name="create_poll"),
    path('create_voting/poll/<int:poll_id>/add_choices', add_choices, name="add_choices"),
    path('vote/<int:survey_id>/', vote, name="vote"),
    path('results/<int:survey_id>/', results, name="results"),
    path('vote_list/', vote_list, name="vote_list"),
    path('poll/<int:poll_id>/choice/<int:choice_id>/delete/', delete_choice, name='delete_choice')
]