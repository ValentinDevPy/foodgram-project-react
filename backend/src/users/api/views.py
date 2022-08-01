from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.api.serializers import UserSerializer, UserCreateSerializer, SetPasswordSerializer
from users.models import User


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer
    
    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user, data=self.request.data)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    
    @action(
        methods=["POST"], detail=False,
        permission_classes=[IsAuthenticated], url_path="set_password"
    )
    def update_password(self, request):
        user = self.request.user
        serializer = SetPasswordSerializer(user, self.request.data)
        if serializer.is_valid():
            user.set_password(serializer.new_password)
