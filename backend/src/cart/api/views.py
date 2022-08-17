from django.db import IntegrityError
from rest_framework import viewsets, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from cart.api.serializers import CreateCartObjectSerializer
from cart.models import Cart


class ShoppingCartViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CreateCartObjectSerializer
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    
    def perform_create(self, serializer):
        try:
            serializer.save(user_id=self.request.user.id, recipe_id=self.kwargs.get("recipe_id"))
        except IntegrityError:
            raise ValidationError({"error": "Already in cart."})
    
    def get_object(self):
        object_in_cart = (
            Cart.objects.get(
                user_id=self.request.user.id,
                recipe_id=self.kwargs.get("recipe_id")
            )
        )
        return object_in_cart
