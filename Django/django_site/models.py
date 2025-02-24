from django.contrib.auth.models import AbstractUser
from django.db import models
from django_site.managers import UserManager

class User(AbstractUser):

    objects: UserManager = UserManager()  # Используем наш кастомный менеджер

    # Указываем уникальные related_name для groups и user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',  # Уникальное имя
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',  # Уникальное имя
        related_query_name='user',
    )

    def __str__(self):
        return self.username
    
class Survey(models.Model):
    name = models.CharField(max_length=120)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)


class Votings(models.Model):
    question = models.CharField(max_length=255)
    survey_id = models.ForeignKey(
        Survey,
        related_name='survey_id',
        on_delete=models.CASCADE,
        null=False,  # Явно указываем, что NULL не допускается в базе данных
        blank=False  # Явно указываем, что поле обязательно в формах
    )

    def __str__(self):
        return self.question
    
class Choice(models.Model):
    poll = models.ForeignKey(Votings, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    
class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.voter} voted for {self.choice}"