from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from app.users.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from app.users.tasks import validate_email
from config.celery_app import get_geo_data, get_holiday
from celery import chain


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ("id", "geo_data", "register_in_holiday", "user_post_count")
        fields = (
            "id",
            "email",
            "first_name",
            "geo_data",
            "register_in_holiday",
            "user_post_count",
        )


class MonoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ("id", "email", "first_name", "user_post_count")
        fields = ("id", "email", "first_name", "user_post_count")


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token["username"] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("password", "password2", "email", "first_name")
        extra_kwargs = {
            "first_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        if validate_email(attrs["email"]) != "DELIVERABLE":
            raise serializers.ValidationError({"email": "This email is not valid."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        chain(get_geo_data.si(user.id) | get_holiday.si(user.id))()

        return user
