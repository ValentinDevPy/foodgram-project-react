from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from cart.models import Cart
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from recipes.utils import bulk_create_recipe_ingredients
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
    id = serializers.PrimaryKeyRelatedField(source='ingredient',
                                            read_only=True)
    name = serializers.SlugRelatedField(slug_field='name',
                                        source='ingredient',
                                        read_only=True)
    measurement_unit = serializers.SlugRelatedField(
        slug_field='measurement_unit',
        source='ingredient', read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeReadSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField()

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
        )

    def get_ingredients(self, obj):
        recipe = obj
        queryset = recipe.recipe_ingredients.all()
        return RecipeIngredientReadSerializer(queryset, many=True).data

    def get_is_in_shopping_cart(self, obj):
        user_id = self.context["request"].user.id
        is_in_shopping_cart = Cart.objects.filter(
            recipe_id=obj.id, user_id=user_id).exists()
        return is_in_shopping_cart


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
        serializer = RecipeReadSerializer(instance)
        return serializer.data

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        ingredients = validated_data.pop("ingredients", None)
        recipe = super(RecipeCreateSerializer, self).create(validated_data)
        bulk_create_recipe_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        self.update_recipe_ingredients(ingredients_data, instance)
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        instance.cooking_time = validated_data.pop('cooking_time')
        instance.tags.set(validated_data.pop('tags'))
        if validated_data.get('image') is not None:
            instance.image = validated_data.pop('image')
        instance.save()
        return instance
