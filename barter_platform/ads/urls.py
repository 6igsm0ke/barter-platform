from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AdViewSet, ExchangeProposalViewSet

app_name = "ads"
router = DefaultRouter()
router.register(r"ads", AdViewSet, basename="ad")
router.register(r"proposals", ExchangeProposalViewSet, basename="proposal")

urlpatterns = router.urls

urlpatterns += []
