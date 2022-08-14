from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
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
        )
    
    def get_ingredients(self, obj):
        recipe = obj
        queryset = recipe.recipe_ingredients.all()
        return RecipeIngredientReadSerializer(queryset, many=True).data


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
    def create_recipe_ingredients(ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe_id=recipe.id,
                ingredient_id=ingredient["id"].id,
                amount=ingredient["amount"],
            )
    
    def to_representation(self, instance):
        serializer = RecipeReadSerializer(instance)
        return serializer.data
    
    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        ingredients = validated_data.pop("ingredients", None)
        recipe = super(RecipeCreateSerializer, self).create(validated_data)
        self.create_recipe_ingredients(ingredients, recipe)
        return recipe
