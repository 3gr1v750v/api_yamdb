from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Title, Category, Genre, User, Comment, Review
from .utils import code_generator


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы не можете добавить более'
                                      'одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = '__all__'


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {'refresh': str(refresh), 'access': str(refresh.access_token)}


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор модели Category."""
    class Meta:
        model = Category
        lookup_field = 'slug'
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор модели Genre."""
    class Meta:
        model = Genre
        lookup_field = 'slug'
        fields = ('name', 'slug')


class TitleViewSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=True)
    category = CategorySerializer(required=True, )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        rating = 0
        reviews = Review.objects.filter(title=obj)
        if reviews:
            for review in reviews:
                rating += review.score
            return rating // reviews.count()
        return None


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор модели Title (кроме метода GET)."""
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug',
    )
    category = CategorySerializer(
        read_only=True,
    )

    class Meta:
        fields = ('id', 'name', 'description', 'year', 'category', 'genre')
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


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
