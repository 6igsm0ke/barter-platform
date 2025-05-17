from django.urls import path
from rest_framework.routers import DefaultRouter


app_name = "ads"
router = DefaultRouter()
# router.register("users", , basename="users")

urlpatterns = router.urls