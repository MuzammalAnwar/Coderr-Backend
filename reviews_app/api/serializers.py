from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Review

User = get_user_model()

class ReviewSerializer(serializers.ModelSerializer):
    """read serializer (and for returning full JSON)."""
    class Meta:
        model = Review
        fields = [
            "id", "business_user", "reviewer",
            "rating", "description",
            "created_at", "updated_at",
        ]
        read_only_fields = ["reviewer", "created_at", "updated_at"]


class ReviewCreateSerializer(serializers.ModelSerializer):
    """POST serializer (validation only)."""
    class Meta:
        model = Review
        fields = ["business_user", "rating", "description"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("rating muss zwischen 1 und 5 liegen.")
        return value

    def validate_business_user(self, business_user):
        if getattr(business_user, "type", None) != "business":
            raise serializers.ValidationError("Es kann nur ein Geschäftsbenutzer bewertet werden.")
        request = self.context.get("request")
        if request and request.user.id == business_user.id:
            raise serializers.ValidationError("Du kannst dich nicht selbst bewerten.")
        return business_user

    def validate(self, attrs):
        request = self.context.get("request")
        if not request:
            return attrs
        if Review.objects.filter(
            reviewer=request.user, business_user=attrs["business_user"]
        ).exists():
            raise serializers.ValidationError(
                "Du hast bereits eine Bewertung für diesen Geschäftsbenutzer abgegeben."
            )
        return attrs


class ReviewUpdateSerializer(serializers.ModelSerializer):
    """PATCH serializer: only rating + description."""
    class Meta:
        model = Review
        fields = ["rating", "description"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("rating muss zwischen 1 und 5 liegen.")
        return value
