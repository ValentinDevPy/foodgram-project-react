from django.db import models

from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        model=User,
        related_name='recipes',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    image = models.ImageField()
    text = models.TextField()
    cooking_time = models.FloatField()


class Ingredient(models.Model):
    GRAM = 'гр'
    KILOGRAM = 'кг'
    MEASUREMENT_UNIT_CHOICES = [
        (GRAM, 'граммы'),
        (KILOGRAM, 'килограммы')
    ]
    name = models.CharField(max_length=255)
    measurement_unit = models.CharField(
        max_length=2,
        choices=MEASUREMENT_UNIT_CHOICES,
        default=GRAM
    )

class Tag(models.Model):
    name = models.CharField(max_length=255)
    hex_code = models.CharField(max_length=7)
    slug = models.CharField(max_length=16)
    

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        model=Recipe,
        related_name='ingredients',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        model=Ingredient,
        related_name='recipes',
        on_delete=models.SET_NULL
    )
