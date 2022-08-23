from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7)
    slug = models.CharField(max_length=16)


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    measurement_unit = models.CharField(max_length=100)


class Recipe(models.Model):
    author = models.ForeignKey(User, related_name="recipes", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="recipes/")
    text = models.TextField()
    cooking_time = models.FloatField(validators=[MinValueValidator(1)])
    tags = models.ManyToManyField(Tag, related_name="tags")
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")
    
    class Meta:
        ordering = ["-id"]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name="recipe_ingredients", on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient, related_name="ingredient_recipes", on_delete=models.CASCADE
    )
    amount = models.FloatField(validators=[MinValueValidator(0)], default=1)

    class Meta:
        unique_together = ("recipe", "ingredient")


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name="users_liked", on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, related_name="favorites", on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("user", "recipe")
