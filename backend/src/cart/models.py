from django.db import models

from recipes.models import Recipe
from users.models import User


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        related_name="cart",
        on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        related_name="in_cart",
        on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'], name='unique cart object')
        ]
