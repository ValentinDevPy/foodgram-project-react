from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from recipes.api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from users.api.views import UserViewSet

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
                path("", include("recipes.api.urls")),
                path("", include(router.urls)),
            ]),
    )]
