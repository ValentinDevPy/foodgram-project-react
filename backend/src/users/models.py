from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscribe(models.Model):
    subscriber = models.ForeignKey(
        model=User,
        related_name='subscribes',
        on_delete=models.CASCADE
    )
    subscribed_for = models.ForeignKey(
        model=User,
        related_name='subscribes',
        on_delete=models.CASCADE
    )
