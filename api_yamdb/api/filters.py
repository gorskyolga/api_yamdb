from django_filters.rest_framework import (
    BaseInFilter, CharFilter, FilterSet, NumberFilter)

from reviews.models import Title


class SlugFilterInFilter(BaseInFilter, CharFilter):
    pass


class TitleFilter(FilterSet):
    category = SlugFilterInFilter(field_name='category__slug',
                                  lookup_expr='in')
    genre = SlugFilterInFilter(field_name='genre__slug', lookup_expr='in')
    name = CharFilter()
    year = NumberFilter()

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
