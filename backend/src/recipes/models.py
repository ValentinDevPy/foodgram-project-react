from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    """Модель тегов рецепта(завтрак,обед,ужин)."""

    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7)
    slug = models.CharField(max_length=16)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Ingredient(models.Model):
    """Модель ингредиентов, которые используются в рецептах."""

    name = models.CharField(max_length=255)
    measurement_unit = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class Recipe(models.Model):
    author = models.ForeignKey(User, related_name="recipes", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="recipes/")
    text = models.TextField()
    cooking_time = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    tags = models.ManyToManyField(Tag, related_name="tags")
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")

    @property
    def added_to_favorite(self):
        return Favorite.objects.filter(recipe_id=self.id).count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name="recipe_ingredients", on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient, related_name="ingredient_recipes", on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)

    def __str__(self):
        return f"В рецепте {self.recipe.name} " f"необходим {self.ingredient.name}."

    class Meta:
        unique_together = ("recipe", "ingredient")
        verbose_name = "Ингредиент для рецепта"
        verbose_name_plural = "Ингредиенты для рецепта"


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name="users_liked", on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, related_name="favorites", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Пользователю {self.user} нравится рецепт {self.recipe.name}"

    class Meta:
        unique_together = ("user", "recipe")
        verbose_name = "Избранный рецепт"
        verbose_name_plural = "Избранные рецепты"
