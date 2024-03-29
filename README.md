# Проект YaMDb

## Описание

Проект создан в рамках учебного курса Яндекс.Практикум.

- Версия проекта, с разворачивание через Docker-compose контейнеры: https://github.com/3gr1v750v/api_yamdb_docker
- Версия проекта, с Docker-compose и настройкой Github Actions Workflow с установкой не сервере Ubuntu : https://github.com/3gr1v750v/api_yamdb_CI

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения
в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
Произведению может быть присвоен жанр из списка предустановленных
(например, «Сказка», «Рок» или «Артхаус»).
Список категорий и жанров может быть расширен администратором.

Аутентифицированные пользователи могут оставлять к произведениям текстовые
отзывы и выставлять произведениям оценку в диапазоне от одного до десяти
(целое число); из пользовательских оценок формируется усреднённая оценка
произведения — рейтинг (целое число). На одно произведение пользователь
может оставить только один отзыв.

Аутентифицированные пользователи также могут оставлять комментарии к отзывам.

### Технологии

- Python 3.7
- Django 3.2
- Django Rest Framework 3.12.4
- Simple JWT
- SQLite3

### Управление пользователями через API

- Регистрация пользователя администратором проекта;
- Самостоятельная регистрация пользователей;
- Передача подтверждающего кода пользователю по электронной почте;
- Присваивание JWT токена пользователю для аутентификации;
- Изменение информации о пользователе;
- Назначение ролей пользователей для управления ресурсами проекта;

### Ресурсы проекта

- Ресурс `auth`: аутентификация.
- Ресурс `users`: пользователи.
- Ресурс `titles`: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс `categories`: категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.
- Ресурс `genres`: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс `reviews`: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс `comments`: комментарии к отзывам. Комментарий привязан к определённому отзыву.

## Документация
Подробное описание ресурсов доступно в документации после запуска проекта по адресу `http://127.0.0.1:8000/redoc/`.

В документации указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры (паджинация, поиск, фильтрация итд.), когда это необходимо.

### Примеры запросов

- Регистрация пользователя:
```
POST /api/v1/auth/signup/
```
- Получение данных своей учетной записи:
```
GET /api/v1/users/me/
```
- Добавление новой категории:
```
POST /api/v1/categories/
```
- Удаление жанра:
```
DELETE /api/v1/genres/{slug}
```
- Частичное обновление информации о произведении:
```
PATCH /api/v1/titles/{titles_id}
```
- Получение списка всех отзывов:
```
GET /api/v1/titles/{title_id}/reviews/
```
- Добавление комментария к отзыву:
```
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

## Как запустить проект:

1. Скопируйте репозиторий и перейдите в него в командной строке:

```
git clone https://github.com/3gr1v750v/api_yamdb
```

```
cd api_yamdb
```

2. Создайте и активируйте виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

3. Установите зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4. Выполните миграции:

```
python manage.py migrate --run-syncdb
```
5. Загрузите тестовые данные:

```
python manage.py load_data_from_csv
```
6. Запуститe проект:

```
python manage.py runserver
```

## Авторы
**Гривцов Евгений** - [https://github.com/3gr1v750v](https://github.com/3gr1v750v)

*Задачи проекта*: Система регистрации и аутентификации; права доступа; работа с токеном; система подтверждения через e-mail.

----
**Пак Владислав** - [https://github.com/PakVla](https://github.com/PakVla)

*Задачи проекта*: Модели, view и эндпойнты для произведений, категорий и жанров. Реализация импорта данных из csv файлов.


----
**Харитонов Тихон** - [https://github.com/TiEnddd](https://github.com/TiEnddd)

*Задачи проекта*: Модели, view и эндпойнты для отзывов, комментариев. Получение рейтинга произведений.
