from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django_site.managers import UserManager
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from src.forms import VoteForm, ChoiceForm, CreatePollForm, CreateSurveyForm
from django_site.models import Votings, Survey, Choice, Vote

User_model = get_user_model()

def main(request: HttpRequest) -> HttpResponse:
    return redirect('home')

@login_required
def vote_list(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        survey = Survey.objects.filter(created_by=request.user)
        context = {
            "Survey" : survey 
        }
    else:
        survey = None
    return render(request, template_name="votings/vote_list.html", context=context)

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

@login_required
def edit_profile(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        request.user.username = request.POST['new_username']
        request.user.set_password(request.POST['new_password'])
        request.user.save()
        return redirect("home")

    return render(request, template_name="edit_profile.html",)

@login_required
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

@login_required
def survey_editor(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)

    context = {
            "survey_name": survey.name,
            "message": "Создайте опрос"
        }

    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            poll: Votings = form.save(commit=False)
            poll.survey_id = survey
            poll.save()
            context['message'] = "Хорошо, теперь добавьте варианты ответов"
            return redirect("add_choices", poll_id=poll.id)
    else:
        form = CreatePollForm()
    
    context['polls'] = survey.survey_id.all()
    context['form'] = form

    votings = context['polls']
    for vote in votings:
        choices = vote.choices.all()  # Добавляем как атрибут объекта
        print(choices)

    print(votings)

    return render(request, 'votings/create_poll.html', context=context)

@login_required
def add_choices(request, poll_id):
    poll: Votings = get_object_or_404(Votings, pk=poll_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.poll = poll
            choice.save()
            return redirect('add_choices', poll_id=poll.id)
    else:
        form = ChoiceForm()
    
    return render(request, 'votings/add_choices.html', {'form': form, 'poll': poll, 'survey_id' : poll.survey_id.id})

def vote(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)

    context = {
        "survey_name": survey.name,
        "message": "Пройди опрос"
    }

    if request.method == 'POST':
        for voting in survey.survey_id.all():
            choice_id = request.POST.get(f'choice_{voting.id}')
            if choice_id:
                choice = Choice.objects.get(id=choice_id)
                # Проверяем, не голосовал ли пользователь уже за этот выбор
                if not Vote.objects.filter(choice=choice, voter=request.user).exists():
                    choice.votes += 1
                    choice.save()
                    Vote.objects.create(choice=choice, voter=request.user)
        return redirect('results', survey_id=survey_id)  # Перенаправляем на результаты

    context['polls'] = survey.survey_id.all()
    return render(request, 'votings/vote.html', context=context)

def results(request, survey_id):
    # Пытаемся получить объект Survey по заданному id
    survey = get_object_or_404(Survey, pk=survey_id)
    context = {

    }
    context['polls'] = survey.survey_id.all()
    return render(request, 'votings/survey_results.html', context)

@login_required
def delete_choice(request, poll_id, choice_id):
    poll = get_object_or_404(Votings, id=poll_id)
    choice = get_object_or_404(Choice, id=choice_id, poll=poll)

    # Проверка, что пользователь — создатель опроса (опционально)
    if poll.survey_id.created_by != request.user:
        return render(request, 'error.html', {'message': 'У вас нет прав для удаления этого варианта.'})

    choice.delete()

    return redirect('add_choices', poll_id=poll.id)