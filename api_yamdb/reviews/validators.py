import datetime
import re

from django.core.exceptions import ValidationError
from django.conf import settings


def username_name_list_validator(value):
    """
    Валидатор для проверки допустимого списка имен пользователей.
    """
    prohibited_usernames = ('me',)
    if value in prohibited_usernames:
        raise ValidationError('Данное имя пользователя нельзя использовать.')


def username_pattern_validation(value):
    """
    Валидатор для проверки паттерна имени пользователя.
    """
    pattern = r"^[\w.@+-]+\Z"
    if not re.search(pattern, value):
        raise ValidationError('Только буквы, цифры и @/./+/-/_ .')


def year_create_validator(value):
    """
    Валидатор для проверки года выпуска произведения.
    """
    if value > datetime.datetime.astimezone(settings.TIME_ZONE).year:
        raise ValidationError('Год выпуска не может быть больше текущего.')
