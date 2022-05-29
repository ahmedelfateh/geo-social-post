from rest_framework import serializers
from app.posts.models import Post
from app.users.serializers import MonoUserSerializer


class PostSerializer(serializers.ModelSerializer):
    user = MonoUserSerializer(read_only=True)

    class Meta:
        model = Post
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "like_count",
            "unlike_count",
        )
        fields = (
            "id",
            "user",
            "body",
            "like",
            "unlike",
            "created_at",
            "updated_at",
            "like_count",
            "unlike_count",
        )


class MonoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "like_count",
            "unlike_count",
        )
        fields = (
            "id",
            "body",
            "like",
            "unlike",
            "created_at",
            "updated_at",
            "like_count",
            "unlike_count",
        )
