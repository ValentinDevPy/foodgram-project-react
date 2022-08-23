from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError, transaction
from rest_framework import serializers, validators
from rest_framework.exceptions import ValidationError

from cart.api.serializers import ShortRecipeSerializer
from recipes.models import Recipe
from users.api.validators import username_validator
from users.models import Subscribe, User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        subscriber_id = self.context["request"].user.id
        is_subscribed = Subscribe.objects.filter(
            subscriber_id=subscriber_id,
            subscribed_for_id=obj.id,
        ).exists()
        return is_subscribed

    class Meta:
        fields = ("email", "id", "username", "first_name", "last_name", "is_subscribed")
        model = User


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        validators=[
            username_validator,
            validators.UniqueValidator(
                queryset=User.objects.all(),
                message="User with this username already exist.",
            ),
        ],
        max_length=150,
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, max_length=150
    )

    default_error_messages = {"cannot_create_user": "Cannot create user. Try again."}

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
        )

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")
        return user

    @staticmethod
    def perform_create(validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
        return user


class SetPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"})
    new_password = serializers.CharField(style={"input_type": "password"})

    default_error_messages = {"invalid_password": "Invalid password!"}

    def validate(self, attrs):
        user = self.context["request"].user or self.user
        if user is None:
            raise ValidationError("Internal error")
        try:
            validate_password(attrs["new_password"], user)
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return super().validate(attrs)

    def validate_current_password(self, value):
        is_password_valid = self.context["request"].user.check_password(value)
        if is_password_valid:
            return value
        else:
            self.fail("invalid_password")


class SubscribeReadSerializer(serializers.ModelSerializer):
    SOURCE_FIELD = "subscribed_for"

    email = serializers.SlugRelatedField(
        read_only=True, source=SOURCE_FIELD, slug_field="email"
    )
    id = serializers.PrimaryKeyRelatedField(read_only=True, source=SOURCE_FIELD)
    username = serializers.SlugRelatedField(
        read_only=True, source=SOURCE_FIELD, slug_field="username"
    )
    first_name = serializers.SlugRelatedField(
        read_only=True, source=SOURCE_FIELD, slug_field="first_name"
    )
    last_name = serializers.SlugRelatedField(
        read_only=True, source=SOURCE_FIELD, slug_field="last_name"
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        subscriber_id = self.context["request"].user.id
        is_subscribed = Subscribe.objects.filter(
            subscriber_id=subscriber_id,
            subscribed_for_id=obj.subscribed_for_id,
        ).exists()
        return is_subscribed

    def get_recipes(self, obj):
        return ShortRecipeSerializer(
            Recipe.objects.filter(author_id=obj.subscribed_for.id), many=True
        ).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author_id=obj.subscribed_for.id).count()

    class Meta:
        model = Subscribe
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )


class SubscribeCreateSerializer(serializers.ModelSerializer):
    subscriber = serializers.PrimaryKeyRelatedField(read_only=True)
    subscribed_for = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_representation(self, instance):
        serializer = SubscribeReadSerializer(
            instance, context={"request": self.context["request"]}
        )
        return serializer.data

    class Meta:
        model = Subscribe
        fields = ("subscriber", "subscribed_for")
