from django.urls import path
from djoser.views import TokenCreateView, TokenDestroyView

app_name = "users"


urlpatterns = [
    path("auth/token/login/", TokenCreateView.as_view()),
    path("auth/token/logout/", TokenDestroyView.as_view()),
]
