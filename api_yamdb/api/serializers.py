from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from reviews.models import Title, Category, Genre, User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {'refresh': str(refresh), 'access': str(refresh.access_token)}

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        lookup_field = 'slug'
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        lookup_field = 'slug'
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, required=False)
    category = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        fields = '__all__'
        model = Title


class ConfirmationCodeSerailizer(serializers.Serializer):
    """Сериализатор для отправки пользователю кода подтверждения."""
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


class EmailAuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(max_length=10)

    # Функция фалидации сериалайзера
    def validate(self, data):
        email = data['email']

        # Если такого еmail в базе нет, вернётся None.
        user = User.objects.filter(email=email).first()

        # Проверяем, что запись в базе есть
        if not user:
            raise serializers.ValidationError(
                {"message": "Пользователь с данным email не зарегистрирован."})

        confirmation_code = data['confirmation_code']

        # Получаем имя пользователя
        username = user.username

        # Код генерится от имени пользователя, сравниваем вводимые данные с эталоном
        confirmation_code_origin = username.encode("utf-8").hex()[:10]

        if confirmation_code == confirmation_code_origin:
            return get_tokens_for_user(user)
        raise serializers.ValidationError(
            {"message": "Введённый код подтверждения не соответствут коду подтверждения пользователя."})


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпоинта user."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
