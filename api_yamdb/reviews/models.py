from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import (
    name_title_validator,
    slug_validator,
    username_validator,
    year_create_validator,
)


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
        (MODERATOR, 'Модератор'),
    ]

    username = models.CharField(
        verbose_name='Пользователь',
        blank=False,
        unique=True,
        max_length=150,
        validators=[username_validator],
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
        default=USER,
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
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_username_email'
            )
        ]

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


class Category(models.Model):
    """Модель, описывающая категории произведений."""

    name = models.CharField(
        verbose_name='Название категории',
        null=False,
        blank=False,
        unique=True,
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Slug категории',
        unique=True,
        max_length=50,
        validators=[slug_validator],
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """Модель, описывающая жанры произведений."""

    name = models.CharField(
        verbose_name='Название жанра',
        null=False,
        blank=False,
        unique=True,
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Slug жанра',
        unique=True,
        max_length=50,
        validators=[slug_validator],
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель, описывающая произведения."""

    name = models.CharField(
        verbose_name='Название произведения',
        null=False,
        blank=False,
        unique=False,
        max_length=256,
        validators=[name_title_validator],
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True,
        null=True,
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        null=False,
        blank=False,
        validators=[year_create_validator],
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория произведения',
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанры произведения',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )

    class Meta:
        verbose_name = 'Жанры произведений'
        verbose_name_plural = 'Жанры произведений'


class Review(models.Model):
    """Модель, описывающая работу отзывов"""

    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10'),
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_review'
            ),
        ]


class Comment(models.Model):
    """Модель, описывающая работу комментариев"""

    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
