from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django_site.managers import UserManager
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from src.forms import VoteForm, ChoiceForm, CreatePollForm, CreateSurveyForm
from django_site.models import Votings, Survey

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
def user_login(request: HttpRequest) -> HttpResponse:
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
        if user is not None:
            login(request, user)
            context["message"] = "Вы успешно вошли в аккаунт"
            return redirect('/home')
        else:
            context["message"] = "Неверный логин или пароль"

    return render(request, template_name="auth.html", context=context)

def profile(request: HttpRequest) -> HttpResponse:
    return render(request, template_name="profile.html",)

@login_required
def user_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")

@login_required
def delete_user(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')
    
    context = {
        "message": "Вы уверены что хотите удалить аккаунт?"
    }
    return render(request, template_name="profile_delete.html", context=context)

def home(request: HttpRequest) -> HttpResponse:
    return render(request, template_name="home.html")

def create_survey(request):
    if request.method == 'POST':
        form = CreateSurveyForm(request.POST)
        if form.is_valid():
            survey: Survey = form.save(commit=False)
            survey.created_by = request.user
            survey.save()  # Сохраняем объект, чтобы получить survey.id
            return redirect('create_poll', survey_id=survey.id)  # Перенаправляем с survey_id
    else:
        form = CreateSurveyForm()
    return render(request, 'votings/create_survey.html', {'form': form})

def survey_editor(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    context = {
            "survey_name": survey.name
        }
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            poll: Votings = form.save(commit=False)
            poll.survey_id = survey
            poll.save()
    else:
        form = CreatePollForm()
    
    context['polls'] = survey.survey_id.all()
    context['form'] = form
    print(context)

    return render(request, 'votings/create_poll.html', context)

def add_choices(request, poll_id):
    poll = get_object_or_404(Votings, pk=poll_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.poll = poll
            choice.save()
            return redirect('add_choices', poll_id=poll.id)
    else:
        form = ChoiceForm()
    return render(request, 'votings/add_choices.html', {'form': form, 'poll': poll})

def vote(request, poll_id):
    poll = get_object_or_404(VoteForm, pk=poll_id)
    if request.method == 'POST':
        form = VoteForm(poll, request.POST)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            VoteForm.objects.create(choice=choice, voter=request.user)
            return redirect('results', poll_id=poll.id)
    else:
        form = VoteForm(poll)
    return render(request, 'votings/vote.html', {'form': form, 'poll': poll})

def results(request, poll_id):
    poll = get_object_or_404(VoteForm, pk=poll_id)
    labels = []
    data = []
    for choice in poll.choices.all():
        labels.append(choice.choice_text)
        data.append(choice.votes.count())
    context = {
        'poll': poll,
        'labels': labels,
        'data': data,
    }
    return render(request, 'results.html', context)