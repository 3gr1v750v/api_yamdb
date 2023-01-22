from django.db import IntegrityError

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Category, Genre
from reviews.models import Comment, Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)


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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )
    title = serializers.HiddenField(default=None)

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)
        validators = [UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=('title', 'author')
        )]

    def create(self, validated_data):
        try:
            review = Review.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {'error': 'Нельзя оставлять два ревью на одно произведение.'})
        return review


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
    genres = GenreSerializer(many=True, required=False)
    category = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        fields = '__all__'
        model = Title
