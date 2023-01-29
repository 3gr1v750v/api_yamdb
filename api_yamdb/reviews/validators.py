import datetime

from django.core.exceptions import ValidationError
from django.conf import settings

def year_create_validator(value):
    """
    Валидатор для проверки года выпуска произведения.
    """
    if value > datetime.datetime.astimezone(settings.TIME_ZONE).year:
        raise ValidationError('Год выпуска не может быть больше текущего.')
