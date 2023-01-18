import re

from django.core.exceptions import ValidationError


def username_validator(value):
    """
    Валидатор для проверки вводимых значений для поля username модели User.
    """
    pattern = r"^[\w.@+-]+\Z"
    prohibited_usernames = ('me', 'admin')
    if not re.search(pattern, value):
        raise ValidationError('Только буквы, цифры и @/./+/-/_ .')
    elif value in prohibited_usernames:
        raise ValidationError('Данное имя пользователя нельзя использовать.')
