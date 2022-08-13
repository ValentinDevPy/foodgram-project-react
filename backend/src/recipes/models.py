from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name="recipes",
        on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField()
    text = models.TextField()
    cooking_time = models.FloatField(validators=[MinValueValidator(1)])


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    measurement_unit = models.CharField(max_length=100)


class Tag(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7)
    slug = models.CharField(max_length=16)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name="ingredients", on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient, related_name="recipes", on_delete=models.CASCADE
    )
    amount = models.FloatField(validators=[MinValueValidator(0)])


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name="tags", on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag,
        related_name="recipes",
        on_delete=models.CASCADE)


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        related_name="favorites",
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, related_name="users_liked", on_delete=models.CASCADE
    )
