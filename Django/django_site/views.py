from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django_site.managers import UserManager
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import redirect

User_model = get_user_model()

def main(request: HttpRequest) -> HttpResponse:
    return redirect('home')

def register(request: HttpRequest) -> HttpResponse:
    context = {
        "title": "Register",
        "zag": "Регистрация",
        "url": "register",
        "submit": "Зарегистрироваться",
        "method": "POST",
        "message": ""
    }
    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['password']
        user = User_model.objects.create_user(name, password)
        if user:
            context["message"] = "Вы успешно зарегались"
            return redirect('login')

    return render(request, template_name="auth.html", context=context)

# Create your views here.
def login(request: HttpRequest) -> HttpResponse:
    context = {
        "title": "Login",
        "zag": "Вход",
        "url": "login",
        "submit": "Войти",
        "method": "POST",
        "message": ""
    }
    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=name, password=password)
        if user:
            context["message"] = "Вы успешно вошли в аккаунт"
        else:
            context["message"] = "Неверный логин или пароль"

    return render(request, template_name="auth.html", context=context)

def home(request: HttpRequest) -> HttpResponse:

    return render(request, template_name="home.html")