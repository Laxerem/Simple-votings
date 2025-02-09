from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        if not username or not password:
            raise ValueError("Заполните все поля")
        else:
            user: AbstractBaseUser = self.model(username=username)
            user.set_password(password)
            user.save(using=self._db)
        return user