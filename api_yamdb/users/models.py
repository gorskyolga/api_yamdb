from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLES_CHOICES = (
        (USER, 'Аутентифицированный пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    email = models.EmailField(
        verbose_name='Электронный адрес',
        help_text=('Обязательное поле. Не более 254 символов. '
                   'Перед @ допустимы буквы и цифры.'),
        max_length=254,
        unique=True,
    )
    bio = models.TextField(
        verbose_name='Биография',
        help_text='Необязательное поле.',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        help_text=('Доступные варианты: Аутентифицированный пользователь, '
                   'Модератор, Администратор.'),
        max_length=9,
        choices=ROLES_CHOICES,
        default=USER,
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    def __str__(self):
        return self.username

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
