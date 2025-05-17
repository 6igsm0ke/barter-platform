from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Ad
from .serializers import AdSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class AdListCreateView(ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)