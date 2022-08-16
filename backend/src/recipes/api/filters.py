import django_filters
from rest_framework import filters

from recipes.models import Recipe, Tag


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug'
    )
    
    class Meta:
        model = Recipe
        fields = ['tags']


class IngredientSeacrh(filters.SearchFilter):
    search_param = "name"
