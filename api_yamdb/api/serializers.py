
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from reviews.models import Title, Category, Genre, GenreTitle, User
from .utils import code_generator


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {'refresh': str(refresh), 'access': str(refresh.access_token)}


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        lookup_field = 'slug'
        fields = ('pk', 'name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        lookup_field = 'slug'
        fields = ('pk', 'name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug'
    )

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        else:
            genres = self.initial_data['genre']
            title = Title.objects.create(**validated_data)
            for genre in genres:
                current_genre = get_object_or_404(Genre, slug=genre)
                GenreTitle.objects.create(
                    title=title, genre=current_genre
                    )
            return title

    class Meta:
        fields = ('pk', 'name', 'description', 'year', 'category', 'genre')
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
