from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "ads"
router = DefaultRouter()
router.register(r"ads", AdViewSet, basename="ad")
router.register(r"proposals", ExchangeProposalViewSet, basename="proposal")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"conditions", ConditionViewSet, basename="condition")

urlpatterns = router.urls

urlpatterns += [
    path("ads/my_ads/", AdViewSet.as_view({"get": "my_ads"}), name="my-ads"),
    path("proposals/my_proposals/", ExchangeProposalViewSet.as_view({"get": "my_proposals"}), name="my-proposals"),
]
