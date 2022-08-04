from rest_framework import serializers

from recipes.models import Tag, Recipe, Ingredient
from users.api.serializers import UserSerializer
from recipes.api.fields import Base64ImageField


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
        read_only=True,
        source="recipe.recipe_tags")
    author = UserSerializer(many=False, read_only=True)
    ingredients = IngredientSerializer(
        many=True, read_only=True, source="recipe.ingredients"
    )
    
    class Meta:
        model = Recipe
        fields = ("id", "tags", "author", "ingredients")


class CreateRecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.RelatedField(many=True, read_only=False, queryset=Ingredient.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    image = Base64ImageField()
    
    class Meta:
        model = Recipe
        fields = ("ingredients", "tags", "image", "name", "text", "cooking_time")
