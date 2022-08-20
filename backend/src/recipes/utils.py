from cart.models import Cart
from recipes.models import RecipeIngredient


def bulk_create_recipe_ingredients(ingredients, recipe) -> None:
    """Создает за один запрос несколько объектов модели RecipeIngredient."""
    RecipeIngredient.objects.bulk_create([RecipeIngredient(
        recipe_id=recipe.id,
        ingredient_id=ingredient["id"].id,
        amount=ingredient["amount"]
    ) for ingredient in ingredients])


def is_in_model(self, obj, model) -> bool:
    """Проверяем, существует ли такой объект в моделях Favorire или Cart."""
    user_id = self.context["request"].user.id
    in_model = model.objects.filter(
        recipe_id=obj.id, user_id=user_id).exists()
    return in_model
