from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_site.models import Choice, Votings, Survey

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password"]  # Поля формы

class CreateSurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['name']

class CreatePollForm(forms.ModelForm):
    class Meta:
        model = Votings
        fields = ['question']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']

class VoteForm(forms.Form):
    choice = forms.ModelChoiceField(queryset=Choice.objects.none(), widget=forms.RadioSelect)

    def __init__(self, poll, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice'].queryset = Choice.objects.filter(poll=poll)