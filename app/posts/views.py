from rest_framework import views, response, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.posts.models import Post
from app.posts.serializers import PostSerializer, MonoPostSerializer


class PostListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        post = Post.objects.create(
            user=request.user,
            **serializer.data,
        )

        return response.Response(
            PostSerializer(post).data, status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        queryset = Post.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PostsAllList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = MonoPostSerializer
    queryset = Post.objects.all()


class PostRetrieveUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = PostSerializer
    lookup_field = "id"

    def get_object(self):
        return generics.get_object_or_404(Post, id=self.kwargs.get("id"))

    def patch(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            return response.Response(
                {"message": "You are not allowed to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.get_object().user != request.user:
            return response.Response(
                {"message": "You are not allowed to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return self.destroy(request, *args, **kwargs)


class LikeUnlikeAPIView(views.APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    serializer_class = PostSerializer
    lookup_field = "id"

    def post(self, request, *args, **kwargs):
        action = kwargs.get("action")
        user_id = request.user.id
        post = generics.get_object_or_404(Post, id=kwargs.get("id"))
        if action == "like":
            if post.unlike:
                post.unlike.remove(user_id)
            if user_id not in post.like:
                post.like.append(user_id)
            else:
                post.like.remove(user_id)
        elif action == "unlike":
            if post.like:
                post.like.remove(user_id)
            if user_id not in post.unlike:
                post.unlike.append(user_id)
            else:
                post.unlike.remove(user_id)
        post.save()
        return response.Response(PostSerializer(post).data, status=status.HTTP_200_OK)
