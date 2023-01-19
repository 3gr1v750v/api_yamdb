import django_filters

from reviews.models import Category, Genre, Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        field_name="category__slug",
        queryset=Category.objects.all()
    )
    genre = django_filters.ModelChoiceFilter(
        field_name="genre__slug",
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
