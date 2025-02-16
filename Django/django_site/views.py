from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django_site.managers import UserManager
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import redirect

User_model = get_user_model()

def main(request: HttpRequest) -> HttpResponse:
    return redirect('home')

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

# Create your views here.
def login(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, name, password)
        if user:
            context = {
                'message': "Вы вошли в аккаунт"
            }

    return render(request, template_name="login.html", context=context)

def home(request: HttpRequest) -> HttpResponse:

    return render(request, template_name="home.html")