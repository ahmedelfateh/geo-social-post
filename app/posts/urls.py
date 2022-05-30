from django.urls import path
from app.posts.views import (
    PostListCreateAPIView,
    PostsAllList,
    PostRetrieveUpdateAPIView,
    LikeUnlikeAPIView,
)

app_name = "posts"

urlpatterns = [
    path("", PostListCreateAPIView.as_view(), name="post_list_create"),
    path("all/", PostsAllList.as_view(), name="post_list_all"),
    path("<int:id>/", PostRetrieveUpdateAPIView.as_view(), name="post_get_update"),
    path(
        "<int:id>/<str:action>/", LikeUnlikeAPIView.as_view(), name="like_unlike_post"
    ),
]
