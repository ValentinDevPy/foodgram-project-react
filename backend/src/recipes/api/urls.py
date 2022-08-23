from django.urls import path

from cart.api.views import ShoppingCartView

urlpatterns = [
    path(
        "recipes/<int:recipe_id>/shopping_cart/",
        ShoppingCartView.as_view()),
]
