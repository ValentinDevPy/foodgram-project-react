from typing import Type, Union

from cart.models import Cart
from recipes.models import Favorite, Recipe, RecipeIngredient


def bulk_create_recipe_ingredients(ingredients, recipe: Recipe) -> None:
    """Создает за один запрос несколько объектов модели RecipeIngredient."""
    RecipeIngredient.objects.bulk_create(
        [
            RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient["id"].id,
                amount=ingredient["amount"],
            )
            for ingredient in ingredients
        ]
    )


def is_in_model(user_id: int, obj: Recipe, model: Type[Union[Favorite, Cart]]) -> bool:
    """Проверяем, существует ли такой объект в моделях Favorite или Cart."""
    in_model = model.objects.filter(recipe_id=obj.id, user_id=user_id).exists()
    return in_model


def update_recipe_instance(self, instance: Recipe, validated_data: dict) -> Recipe:
    ingredients_data = validated_data.pop("ingredients")
    self.update_recipe_ingredients(ingredients_data, instance)
    instance.name = validated_data.pop("name")
    instance.text = validated_data.pop("text")
    instance.cooking_time = validated_data.pop("cooking_time")
    instance.tags.set(validated_data.pop("tags"))
    if validated_data.get("image") is not None:
        instance.image = validated_data.pop("image")
    instance.save()
    return instance
