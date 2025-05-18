from rest_framework import serializers
from .models import Ad, Category, Condition, ExchangeProposal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ["id", "name"]


class AdSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    condition = serializers.PrimaryKeyRelatedField(queryset=Condition.objects.all())

    class Meta:
        model = Ad
        fields = [
            "id",
            "user",
            "title",
            "description",
            "image_url",
            "category",
            "condition",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = CategorySerializer(instance.category).data
        data["condition"] = ConditionSerializer(instance.condition).data
        return data

class ProposalSerializer(serializers.ModelSerializer):
    ad_sender = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())
    ad_receiver = serializers.PrimaryKeyRelatedField(queryset=Ad.objects.all())

    class Meta:
        model = ExchangeProposal
        fields = [
            "id",
            "ad_sender",
            "ad_receiver",
            "comment",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "status"]