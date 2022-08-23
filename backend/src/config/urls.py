from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from cart.api.views import ShoppingCartView
from recipes.api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.api.views import SubscribeListView, SubscribeView, UserViewSet

router = routers.DefaultRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"tags", TagViewSet, basename="tags")
router.register(r"recipes", RecipeViewSet, basename="recipes")
router.register(r"ingredients", IngredientViewSet, basename="ingredients")

urlpatterns = [
    path(
        "api/",
        include(
            [
                path("admin/", admin.site.urls),
                path("", include("users.api.urls")),
                path(
                    "recipes/<int:recipe_id>/shopping_cart/",
                    ShoppingCartView.as_view()),
                path(
                    "users/subscriptions/",
                    SubscribeListView.as_view()),
                path(
                    "users/<int:user_id>/subscribe/",
                    SubscribeView.as_view()),
                path("", include(router.urls)),
            ]),
    )]

