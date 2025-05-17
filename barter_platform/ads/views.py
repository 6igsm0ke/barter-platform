from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Ad
from .serializers import AdSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class AdListCreateView(ListCreateAPIView):
    """
    View to list and create ads.
    """
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]