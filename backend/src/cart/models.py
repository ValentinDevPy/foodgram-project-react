from django.db import models

from recipes.models import Recipe
from users.models import User


class Cart(models.Model):
    """Модель корзины рецептов."""

    user = models.ForeignKey(
        User,
        related_name="cart",
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="in_cart",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Рецепт {self.recipe} в корзине у пользователя {self.user}"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique cart object"
            )
        ]
