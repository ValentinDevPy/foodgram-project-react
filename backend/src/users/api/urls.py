from django.urls import path
from djoser.views import TokenCreateView, TokenDestroyView

from users.api.views import SubscribeListView, SubscribeView

app_name = "users"


urlpatterns = [
    path("auth/token/login/", TokenCreateView.as_view()),
    path("auth/token/logout/", TokenDestroyView.as_view()),
    path(
        "users/subscriptions/",
        SubscribeListView.as_view()),
    path(
        "users/<int:user_id>/subscribe/",
        SubscribeView.as_view()),
]
