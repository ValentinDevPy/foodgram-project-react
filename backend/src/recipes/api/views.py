from rest_framework import mixins, viewsets

from recipes.api.serializers import TagSerializer, RecipeSerializer, CreateRecipeSerializer
from recipes.models import Tag, Recipe


class TagViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrive":
            return RecipeSerializer
        return CreateRecipeSerializer
    
    
