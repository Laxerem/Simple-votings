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