from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.api.serializers import (SetPasswordSerializer, UserCreateSerializer,
                                   UserSerializer)
from users.models import User


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

    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, request, *args, **kwargs):
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = UserSerializer(self.object)
        return Response(serializer.data)

    @action(
        ["post"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="set_password",
    )
    def update_password(self, request):
        user = self.request.user
        serializer = SetPasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(
                {"status": "password set"}, status=status.HTTP_204_NO_CONTENT
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
