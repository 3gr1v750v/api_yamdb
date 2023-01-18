from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import username_validator


class User(AbstractUser):
    """
    Переопределение модели User. Модель расширена свойствами role и bio.
    Любой пользователь может получить одну из 3х ролей управления. Только
    superuser получает права доступа к административной части сайта, при этом
    изменение его пользовательской роли не влияет вышеуказанные права.
    Обычный пользователь получив роль 'admin' может осуществлять управление
    пользователя через API без доступа к административной части сайта.
    """

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    USER_ROLE = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор')
    ]

    username = models.CharField(
        verbose_name='Пользователь',
        blank=False,
        unique=True,
        max_length=150,
        validators=[username_validator]
    )

    email = models.EmailField(
        verbose_name='Почтовый адрес',
        blank=False,
        unique=True,
        max_length=254,
    )

    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True,
    )

    role = models.CharField(
        verbose_name='Роль пользователя',
        max_length=20,
        choices=USER_ROLE,
        default=USER
    )

    first_name = models.CharField(
        verbose_name="Имя пользователя",
        max_length=150,
        blank=True,
        null=True,
    )

    last_name = models.CharField(
        verbose_name="Фамилия пользователя",
        max_length=150,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_admin(self):
        if self.role == self.ADMIN:
            return True
        else:
            return False

    @property
    def is_moderator(self):
        if self.role == self.MODERATOR:
            return True
        else:
            return False
