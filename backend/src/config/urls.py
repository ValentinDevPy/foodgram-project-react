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
    path("api/admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include("users.api.urls"))
]
