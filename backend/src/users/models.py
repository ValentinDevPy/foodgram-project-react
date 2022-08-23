from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

User = get_user_model()


class Subscribe(models.Model):
    subscriber = models.ForeignKey(
        User, related_name="subscribes", on_delete=models.CASCADE
    )
    subscribed_for = models.ForeignKey(
        User,
        related_name="subscribed_for",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["subscriber", "subscribed_for"], name="unique subscribe object"
            )
        ]
