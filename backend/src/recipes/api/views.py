from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.response import Response

from cart.api.serializers import ShortRecipeSerializer
from recipes.api.filters import IngredientSeacrh, RecipeFilter
from recipes.api.serializers import (IngredientSerializer,
                                     RecipeCreateSerializer,
                                     RecipeReadSerializer, TagSerializer)
from recipes.models import Favorite, Ingredient, Recipe, Tag


class TagViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return RecipeReadSerializer
        return RecipeCreateSerializer

    @action(methods=["post", "delete"], detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user_id = request.user.id

        if request.method == "POST":
            try:
                Favorite.objects.create(
                    user_id=user_id,
                    recipe_id=recipe.id,
                )
            except IntegrityError:
                raise ValidationError({"error": "already liked."})
            instance = Recipe.objects.get(pk=pk)
            response_data = ShortRecipeSerializer(instance=instance).data
            return Response(data=response_data, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            favorite_object = Favorite.objects.filter(
                user_id=user_id, recipe_id=recipe.id
            )
            if favorite_object.exists():
                favorite_object.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class IngredientViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientSeacrh,)
    search_fields = ("name",)
