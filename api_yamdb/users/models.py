from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES_CHOICES = [
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    ]

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Электронный адрес',
        max_length=254,
        blank=True,
        unique=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=9,
        choices=ROLES_CHOICES,
        default=USER,
    )
    confirmation_code = models.CharField(max_length=32)

    def __str__(self):
        return self.username
