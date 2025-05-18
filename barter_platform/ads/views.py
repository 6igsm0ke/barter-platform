from django.shortcuts import render
from rest_framework import generics, filters, viewsets, permissions
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ProposalSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action


# Create your views here.


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "description"]
    filterset_fields = ["category", "condition"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You are not allowed to update this ad.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You are not allowed to delete this ad.")
        instance.delete()

    @action(detail=False, methods=["get"])
    def my_ads(self, request):
        ads = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(ads, many=True)
        return Response(serializer.data)


class ExchangeProposalListCreateView(generics.ListCreateAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["ad_sender", "ad_receiver", "status"]

    def perform_create(self, serializer):
        serializer.save()


class ExchangeProposalUpdateView(generics.UpdateAPIView):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]
