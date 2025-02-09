from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django_site.managers import UserManager
from django.contrib.auth import get_user_model

User_model = get_user_model()

# Create your views here.
def register(request: HttpRequest) -> HttpResponse:
    return render(request, template_name="register.html")

def home(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['password']
        user = User_model.objects.create_user(name, password)

    return render(request, template_name="home.html")