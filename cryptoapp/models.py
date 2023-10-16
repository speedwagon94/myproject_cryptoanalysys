from django.db import models
from django.contrib.auth.models import AbstractUser


# Модель для запросов пользователей.
class UserRequest(models.Model):
    """
    Модель для хранения запросов пользователей.
    """
    symbol = models.CharField(max_length=255)
    interval = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.symbol}, {self.interval}'


# Модель новостей.
class News(models.Model):
    """
    Модель для хранения новостей.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateField('date published')

    def __str__(self):
        return self.title
