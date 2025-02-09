from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django_site.managers import UserManager
from django.contrib.auth import get_user_model

User_model = get_user_model()

# Create your views here.
def register(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['password']
        user = User_model.objects.create_user(name, password)
        if user:
            context = {
                'message': "Ваш аккаунт зарегистрирован"
            }

    return render(request, template_name="register.html", context=context)

def login(request: HttpRequest) -> HttpResponse:
    return render(request, template_name="login.html")

def home(request: HttpRequest) -> HttpResponse:

    return render(request, template_name="home.html")