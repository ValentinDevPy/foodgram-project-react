from recipes.models import RecipeIngredient


def bulk_create_recipe_ingredients(ingredients, recipe):
    RecipeIngredient.objects.bulk_create([RecipeIngredient(
        recipe_id=recipe.id,
        ingredient_id=ingredient["id"].id,
        amount=ingredient["amount"]
    ) for ingredient in ingredients])