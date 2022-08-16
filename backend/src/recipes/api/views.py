from rest_framework import mixins, viewsets, permissions

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
    
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return RecipeReadSerializer
        return RecipeCreateSerializer
    
    def get_queryset(self):
        queryset = Recipe.objects.all()
        tags = self.request.query_params.get('tags')
        if tags is not None:
            queryset.filter(tags__in=tags)
            print(tags)
        
        return queryset


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
