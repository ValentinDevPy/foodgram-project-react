from django.urls import path

from users.api.views import SubscribeListView, SubscribeView

urlpatterns = [
    path(
        "users/subscriptions/",
        SubscribeListView.as_view()),
    path(
        "users/<int:user_id>/subscribe/",
        SubscribeView.as_view()),
]
