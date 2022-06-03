import django_filters

from review.models import Title


class TitlesFilter(django_filters.FilterSet):
    genres = django_filters.CharFilter(field_name='genres', lookup_expr='slug')
    category = django_filters.CharFilter(field_name='category', lookup_expr='slug')

    class Meta:
        model = Title
        fields = ['genres', 'category', 'year', 'title_name']