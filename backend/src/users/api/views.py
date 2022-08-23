from django.db import IntegrityError
from rest_framework import generics, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.api.serializers import (
    SetPasswordSerializer,
    SubscribeCreateSerializer,
    SubscribeReadSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from users.models import Subscribe, User


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = UserSerializer(self.object, context={"request": request})
        return Response(serializer.data)

    @action(
        ["post"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="set_password",
    )
    def update_password(self, request):
        user = self.request.user
        serializer = SetPasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(
            {"status": "password set"}, status=status.HTTP_204_NO_CONTENT
        )


class SubscribeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, user_id):
        data = {"subscriber": request.user.id, "subscribed_for": user_id}
        serializer = SubscribeCreateSerializer(
            data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        subscriber_id = request.user.id
        subscribed_for = get_object_or_404(User, id=user_id)
        Subscribe.objects.filter(
            subscriber_id=subscriber_id, subscribed_for_id=subscribed_for.id
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscribeReadSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_queryset(self):
        user_id = self.request.user.id
        recipes_limit = self.request.query_params.get("recipes_limit")
        subscribes = Subscribe.objects.filter(subscriber_id=user_id)
        if recipes_limit:
            return subscribes[:int(recipes_limit)]
        else:
            return subscribes
