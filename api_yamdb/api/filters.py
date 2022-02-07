import django_filters
from reviews.models import Title


class TitlesFilter(django_filters.FilterSet):

    genre = django_filters.CharFilter(field_name='genre__slug', lookup_expr='icontains')
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
