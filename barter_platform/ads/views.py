from django.shortcuts import render
from rest_framework import generics, filters, viewsets, permissions
from django.db import models
from .models import Ad, ExchangeProposal
from .serializers import AdSerializer, ProposalSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


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


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["ad_sender__title", "ad_receiver__title", "comment"]
    filterset_fields = ["ad_sender", "ad_receiver", "status"]

    def perform_create(self, serializer):
        sender_ad = serializer.validated_data.get("ad_sender")
        if sender_ad.user != self.request.user:
            raise PermissionDenied("You can only send proposals from your own ads.")
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(
            models.Q(ad_sender__user=user) | models.Q(ad_receiver__user=user)
        )

    def perform_update(self, serializer):
        proposal = self.get_object()
        if proposal.ad_receiver.user != self.request.user:
            raise PermissionDenied("Only the receiver can update this proposal.")
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        # только получатель может обновить статус
        if instance.ad_receiver.user != request.user:
            return Response(
                {"detail": "You are not allowed to change status of this proposal."},
                status=status.HTTP_403_FORBIDDEN,
            )

        status_value = request.data.get("status")
        if status_value not in ["accepted", "rejected"]:
            return Response(
                {"detail": "Invalid status value."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        instance.status = status_value
        instance.save()
        return Response(ProposalSerializer(instance).data)
