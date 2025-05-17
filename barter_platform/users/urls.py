from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

app_name = "users"
router = DefaultRouter()
# router.register("users", UserViewSet, basename="users")

urlpatterns = router.urls