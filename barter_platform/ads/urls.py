from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AdViewSet

app_name = "ads"
router = DefaultRouter()
router.register("ads", AdViewSet, basename="ads")

urlpatterns = router.urls

urlpatterns += [
]