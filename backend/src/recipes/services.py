from typing import Type, Union

from django.db.models import Sum

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


def is_in_model(user_id: int, obj: Recipe,
                model: Type[Union[Favorite, Cart]]) -> bool:
    """Проверяем, существует ли такой объект в моделях Favorite или Cart."""
    in_model = model.objects.filter(recipe_id=obj.id, user_id=user_id).exists()
    return in_model


def update_recipe_ingredients(ingredients, recipe):
    RecipeIngredient.objects.filter(recipe_id=recipe.id).delete()
    bulk_create_recipe_ingredients(ingredients, recipe)


def get_shopping_list_txt(user_id: int) -> list:
    ingredients = (
        Recipe.objects
        .filter(in_cart__user_id=user_id)
        .select_related("ingredients", "recipe_ingredients")
        .values("ingredients__name", "ingredients__measurement_unit")
        .annotate(sum=Sum("recipe_ingredients__amount"))
    )

    ingredient_txt = [
        (
            f"{item['ingredients__name']} \u2014 "
            f"{int(item['sum'])} {item['ingredients__measurement_unit']}\n"
        )
        for item in ingredients
    ]
    return ingredient_txt
