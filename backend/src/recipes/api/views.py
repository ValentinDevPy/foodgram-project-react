from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.decorators import action

from recipes.api.filters import RecipeFilter, IngredientSeacrh
from recipes.api.serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer, TagSerializer
)
from recipes.models import Ingredient, Recipe, Tag


class TagViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return RecipeReadSerializer
        return RecipeCreateSerializer
    
    @action(methods=["post", "delete"], detail=True)
    def shopping_cart(self, request, pk=None):
        pass


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientSeacrh,)
    search_fields = ('name',)
