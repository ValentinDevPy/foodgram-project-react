from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.api.serializers import CreateCartObjectSerializer
from cart.models import Cart
from recipes.models import Recipe


class ShoppingCartView(APIView):
    """Логика работы корзины."""

    permission_classes = [IsAuthenticated]

    def post(self, request, recipe_id):
        data = {"user": request.user.id, "recipe": recipe_id}
        serializer = CreateCartObjectSerializer(
            data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user_id = request.user.id
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Cart.objects.filter(user_id=user_id, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
