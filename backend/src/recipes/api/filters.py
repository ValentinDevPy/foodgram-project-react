import django_filters.rest_framework as django_filters
from rest_framework import filters

from recipes.models import Recipe, Tag


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        queryset=Tag.objects.all(),
        to_field_name="slug")
    is_favorited = django_filters.BooleanFilter(method="get_is_favorited")
    is_in_shopping_cart = django_filters.BooleanFilter(
        method="get_is_in_shopping_cart")

    class Meta:
        model = Recipe
        fields = [
            "tags",
            "author",
            "is_favorited",
            "is_in_shopping_cart",
        ]

    def get_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(in_cart__user=self.request.user)
        return queryset


class IngredientSeacrh(filters.SearchFilter):
    search_param = "name"
