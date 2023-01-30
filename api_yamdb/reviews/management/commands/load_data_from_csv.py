import csv

from django.conf import settings
from django.core.management import BaseCommand
from django.db import IntegrityError
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User

FILES_CLASSES = {
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'genre_title': GenreTitle,
    'users': User,
    'review': Review,
    'comments': Comment,
}

FIELDS = {
    'category': ('category', Category),
    'title_id': ('title', Title),
    'genre_id': ('genre', Genre),
    'author': ('author', User),
    'review_id': ('review', Review),
}


def open_csv_file(file_name):
    """Метод считывания csv-файлов."""
    try:
        with (
            open(settings.PATH_CSV_FILES[file_name], encoding='utf-8')
        ) as file:
            return list(csv.reader(file))

    except FileNotFoundError:
        print(f'Файл {file_name}.csv не найден.')


def change_foreign_values(data_csv):
    """Изменение значений полей в считанных данных."""
    data_csv_copy = data_csv.copy()
    for field_key, field_value in data_csv.items():
        if field_key in FIELDS.keys():
            field_model = FIELDS[field_key][0]

            data_csv_copy[field_model] = FIELDS[field_key][1].objects.get(
                pk=field_value
            )
    return data_csv_copy


def load_csv(file_name, class_name):
    """Осуществляет загрузку данных из csv-файлов в модели."""
    data = open_csv_file(file_name)
    rows = data[1:]
    for row in rows:
        data_csv = change_foreign_values(dict(zip(data[0], row)))
        try:
            table = class_name(**data_csv)
            table.save()
        except (ValueError, IntegrityError) as error:
            print(
                f'Ошибка в загружаемых данных. {error}. '
                f'Данные в таблицу {class_name.__qualname__} не загружены.'
            )
            break
    print(f'Данные в таблицу {class_name.__qualname__} загружены.')


class Command(BaseCommand):
    """Класс для создания новой команды на добавление данных из csv файлов."""

    def handle(self, *args, **options):
        for key, value in FILES_CLASSES.items():
            load_csv(key, value)
