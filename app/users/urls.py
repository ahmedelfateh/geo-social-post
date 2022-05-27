from django.urls import path
from app.users.views import (
    MyObtainTokenPairView,
    RegisterView,
    UserRetrieveUpdateAPIView,
)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth_register"),
    path("login/", MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", UserRetrieveUpdateAPIView.as_view()),
]
