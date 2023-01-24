from rest_framework import serializers
from django.shortcuts import get_object_or_404

from reviews.models import Title, Category, Genre, GenreTitle


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
