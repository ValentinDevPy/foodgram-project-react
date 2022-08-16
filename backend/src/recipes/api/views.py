from rest_framework import mixins, viewsets, permissions, filters

from django_filters.rest_framework import DjangoFilterBackend

from recipes.api.filters import RecipeFilter
from recipes.api.serializers import TagSerializer, RecipeReadSerializer, RecipeCreateSerializer, IngredientSerializer
from recipes.models import Tag, Recipe, Ingredient


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


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
