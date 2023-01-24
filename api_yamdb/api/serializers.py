from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from reviews.models import Title, Category, Genre, User
from .utils import code_generator


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


class ConfirmationCodeSerailizer(serializers.ModelSerializer):
    """Сериализатор для отправки пользователю кода подтверждения."""
    class Meta:
        model = User
        fields = (
            'username', 'email'
        )


class EmailAuthSerializer(serializers.Serializer):
    """Сериализатор для получения токена по коду подтверждения."""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=10)

    def validate(self, data):
        username = data['username']
        user = get_object_or_404(User, username=username)

        confirmation_code = data['confirmation_code']
        confirmation_code_origin = code_generator(username)

        if confirmation_code == confirmation_code_origin:
            return get_tokens_for_user(user)
        raise serializers.ValidationError(
            {"message": ("Введённый код подтверждения не "
                         "соответствут коду подтверждения пользователя.")})


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпоинта user."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
