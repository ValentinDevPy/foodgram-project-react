from rest_framework import serializers, status
from rest_framework.response import Response

from recipes.models import Tag, Recipe, Ingredient, RecipeIngredient, RecipeTag
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


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    
    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount")


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    cooking_time = serializers.IntegerField(min_value=0)
    
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
    
    def get_tags(self, obj):
        return TagSerializer(
            Tag.objects.filter(recipes__recipe_id=obj.id),
            many=True
        ).data
    
    def get_ingredients(self, obj):
        return IngredientSerializer(
            Ingredient.objects.filter(recipes__recipe_id=obj.id),
            many=True
        ).data


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    ingredients = RecipeIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()
    
    class Meta:
        model = Recipe
        fields = "__all__"
    
    @staticmethod
    def create_tags_and_ingredients(recipe, ingredients, tags):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe_id=recipe.id, ingredient_id=ingredient["id"].id, amount=ingredient["amount"]
            )
        
        for tag in tags:
            RecipeTag.objects.create(
                recipe_id=recipe.id, tag_id=tag.id
            )
    
    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        ingredients = validated_data.pop("ingredients", None)
        tags = validated_data.pop("tags", None)
        recipe = super().create(validated_data)
        self.create_tags_and_ingredients(recipe, ingredients, tags)
        return recipe

    def to_representation(self, obj):
        data = RecipeReadSerializer(data=self.validated_data).is_valid(raise_exception=True)
        data['image'] = obj.image.url
        return data
