from django_filters import FilterSet, AllValuesFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    category = AllValuesFilter(field_name='category__slug')
    genre = AllValuesFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
