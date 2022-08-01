from django.urls import path, include
from rest_framework import routers

from users.api.views import UserViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path("", include(router.urls)),
    path("", include('djoser.urls.base')),
    
]
