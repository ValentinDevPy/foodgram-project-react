from django.db import models

from users.models import User
from recipes.models import Recipe


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        related_name="cart",
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        related_name="in_cart",
        on_delete=models.CASCADE)
