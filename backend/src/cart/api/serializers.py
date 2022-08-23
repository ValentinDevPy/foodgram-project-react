from rest_framework import serializers

from cart.models import Cart
from recipes.models import Recipe


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class CreateCartObjectSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    recipe_id = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Cart
        fields = ["user_id", "recipe_id"]

    def to_representation(self, instance):
        serializer = ShortRecipeSerializer(instance.recipe)
        return serializer.data
