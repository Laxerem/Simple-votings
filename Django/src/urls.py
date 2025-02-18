from django.contrib import admin
from django.urls import path
from django_site.views import register, home, user_login, main, profile, user_logout, delete_user, edit_profile

urlpatterns = [
    path("", main, name="main"),
    path('register', register, name="register"),
    path('login', user_login, name="login"),
    path('home', home, name="home"),
    path('profile', profile, name="profile"),
    path('logout/', user_logout, name="logout"),
    path('delete/user/', delete_user, name="profile_delete"),
    path('user/edit_profile', edit_profile, name="edit_profile"),
]