from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from cart.models import Cart
from recipes.models import Recipe


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class CreateCartObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=Cart.objects.all(), fields=["recipe", "user"]
            )
        ]

    def to_representation(self, instance):
        serializer = ShortRecipeSerializer(
            instance.recipe, context={"request": self.context["request"]}
        )
        return serializer.data
