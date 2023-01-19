from rest_framework import serializers

from reviews.models import Title, Category, Genre


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
    username = serializers.CharField()
    email = serializers.EmailField()
