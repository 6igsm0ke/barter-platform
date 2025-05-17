from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter


app_name = "users"
router = DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = router.urls

urlpatterns += [
    path("register/", UserCreateView.as_view(), name="user_create"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]