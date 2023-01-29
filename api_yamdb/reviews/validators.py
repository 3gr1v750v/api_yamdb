import datetime
import re

from django.core.exceptions import ValidationError
from django.conf import settings

def username_validator(value):
    """
    Валидатор для проверки вводимых значений для поля username модели User.
    """
    pattern = r"^[\w.@+-]+\Z"
    prohibited_usernames = ('me',)
    if not re.search(pattern, value):
        raise ValidationError('Только буквы, цифры и @/./+/-/_ .')
    elif value in prohibited_usernames:
        raise ValidationError('Данное имя пользователя нельзя использовать.')


def year_create_validator(value):
    """
    Валидатор для проверки года выпуска произведения.
    """
    if value > datetime.datetime.astimezone(settings.TIME_ZONE).year:
        raise ValidationError('Год выпуска не может быть больше текущего.')
