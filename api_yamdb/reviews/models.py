from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import username_validator, year_create_validator, \
    slug_validator


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


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        null=False,
        blank=False,
        unique=True,
        max_length=256
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        validators=[slug_validator]
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        null=False,
        blank=False,
        unique=True,
        max_length=256
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        validators=[slug_validator]
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        null=False,
        blank=False,
        unique=True,
        max_length=256
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
        validators=[year_create_validator]
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True
    )
    genres = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        blank=False,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews')
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField('Отзыв')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    score = models.PositiveSmallIntegerField(
        'Рейтинг', validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_review"
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments')
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments')
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
