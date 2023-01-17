from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Переопределение модели User. Модель расширена свойствами role и bio.
    Также переопределен метод save для координации роли пользователя и прав
    администрирования сайта.
    """

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    USER_ROLE = [
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор')
    ]

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

    def save(self, *args, **kwargs):
        """
        'Пользователь' получает доступ к разделу администрирования при
        изменении роли на 'Администратор', так и наоборот.
        'Суперпользователь' получает права администратора. Даже если изменить
        пользовательскую роль 'суперпользователя'— это не лишит его прав
        администратора.
        """

        if self.role == self.ADMIN or self.is_superuser:
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)
