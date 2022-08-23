from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from cart.models import Cart
from recipes.models import Favorite, Ingredient, Recipe, RecipeIngredient, Tag
from recipes.services import (bulk_create_recipe_ingredients, is_in_model,
                              update_recipe_instance)
from users.api.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source="ingredient", read_only=True)
    name = serializers.SlugRelatedField(
        slug_field="name", source="ingredient", read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        slug_field="measurement_unit", source="ingredient", read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "cooking_time",
            "text",
            "is_in_shopping_cart",
            "is_favorited",
        )

    def get_ingredients(self, obj):
        queryset = obj.recipe_ingredients.all()
        return RecipeIngredientReadSerializer(queryset, many=True).data

    def get_is_in_shopping_cart(self, obj):
        user_id = self.context["request"].user.id
        return is_in_model(user_id, obj, Cart)

    def get_is_favorited(self, obj):
        user_id = self.context["request"].user.id
        return is_in_model(user_id, obj, Favorite)


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    ingredients = RecipeIngredientSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = "__all__"

    @staticmethod
    def update_recipe_ingredients(ingredients, recipe):
        RecipeIngredient.objects.filter(recipe_id=recipe.id).delete()
        bulk_create_recipe_ingredients(ingredients, recipe)

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(
            instance, context={"request": self.context["request"]}
        )
        return serializer.data

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        ingredients = validated_data.pop("ingredients", None)
        recipe = super(RecipeCreateSerializer, self).create(validated_data)
        bulk_create_recipe_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance = update_recipe_instance(self, instance, validated_data)
        return instance
