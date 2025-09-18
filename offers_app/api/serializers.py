from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from django.urls import reverse
from django.utils.functional import cached_property
from rest_framework.reverse import reverse as drf_reverse


class OfferDetailSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2,  coerce_to_string=False)

    class Meta:
        model = OfferDetail
        fields = ("id", "title", "revisions", "delivery_time_in_days",
                  "price", "features", "offer_type")

    def validate_features(self, value):
        if value is None:
            return []
        if not isinstance(value, list):
            raise serializers.ValidationError("features must be a JSON array.")
        cleaned = []
        for item in value:
            if not isinstance(item, str):
                raise serializers.ValidationError(
                    "All features must be strings.")
            s = item.strip()
            if s:
                cleaned.append(s)
        return cleaned


class OfferListItemSerializer(serializers.ModelSerializer):
    # show creator id as "user" to mirror the docs
    user = serializers.IntegerField(source="business_user_id", read_only=True)

    # links to details as list of {id, url}
    details = serializers.SerializerMethodField()

    # annotated values provided by the view/queryset
    min_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True,  coerce_to_string=False)
    min_delivery_time = serializers.IntegerField(read_only=True)

    # summarized creator info
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = (
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        )

    def get_details(self, obj):
        request = self.context.get("request")
        items = []
        # we assume you have a detail route named "offerdetail-detail": /api/offerdetails/<id>/
        for d in getattr(obj, "details_all", None) or obj.details.all():
            url = reverse("offerdetail-detail", args=[d.id], request=request) if hasattr(
                self, "request") else reverse("offerdetail-detail", args=[d.id])
            items.append({"id": d.id, "url": url})
        return items

    def get_user_details(self, obj):
        u = obj.business_user
        return {
            "first_name": getattr(u, "first_name", "") or "",
            "last_name": getattr(u, "last_name", "") or "",
            "username": getattr(u, "username", "") or "",
        }


class OfferSerializer(serializers.ModelSerializer):
    """
    WRITE serializer (POST/PUT/PATCH). For PATCH you can send a subset of fields.
    For details, send any subset; each item must include either 'id' or 'offer_type'
    so we can find the correct OfferDetail to update.
    """
    details = OfferDetailSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ("id", "title", "image", "description",
                  "details", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")

    def validate_details(self, value):
        # Enforce exactly 3 tiers only on CREATE (no instance yet) or full update
        if not getattr(self, "partial", False) and self.instance is None:
            required = {"basic", "standard", "premium"}
            got = {d.get("offer_type") for d in value}
            if len(value) != 3 or got != required:
                raise serializers.ValidationError(
                    "details must include exactly one of each: basic, standard, premium."
                )
        return value

    def create(self, validated_data):
        details_data = validated_data.pop("details", [])
        user = getattr(self.context.get("request"), "user", None)
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")
        if getattr(user, "type", None) != "business":
            raise serializers.ValidationError(
                "Only business users can create offers.")
        offer = Offer.objects.create(business_user=user, **validated_data)
        OfferDetail.objects.bulk_create(
            [OfferDetail(offer=offer, **d) for d in details_data])
        offer.refresh_from_db()
        return offer

    def update(self, instance, validated_data):
        # Simple field updates
        for f in ("title", "image", "description"):
            if f in validated_data:
                setattr(instance, f, validated_data[f])

        # Partial updates for details (optional)
        details_data = validated_data.get("details")
        if details_data is not None:
            for d in details_data:
                # identify the detail row
                od = None
                if "id" in d:
                    od = instance.details.filter(pk=d["id"]).first()
                elif "offer_type" in d:
                    od = instance.details.filter(
                        offer_type=d["offer_type"]).first()
                if not od:
                    raise serializers.ValidationError(
                        "Each detail must include a valid 'id' or 'offer_type'.")

                # update allowed fields
                for f in ("title", "revisions", "delivery_time_in_days", "price", "features"):
                    if f in d:
                        setattr(od, f, d[f])
                od.save()

        instance.save()
        return instance


class OfferReadSerializer(serializers.ModelSerializer):
    """
    READ serializer (GET list/detail). Returns:
    - user = business_user_id
    - details = [{id, url}]
    - min_price (int), min_delivery_time (int)
    """
    user = serializers.IntegerField(source="business_user_id", read_only=True)
    details = serializers.SerializerMethodField()
    min_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True, coerce_to_string=False)
    min_delivery_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Offer
        fields = (
            "id", "user", "title", "image", "description",
            "created_at", "updated_at",
            "details", "min_price", "min_delivery_time",
        )

    def get_details(self, obj):
        request = self.context.get("request")
        rel = getattr(obj, "_prefetched_objects_cache", {}
                      ).get("details", obj.details.all())
        return [{"id": d.id, "url": drf_reverse("offerdetail-detail", args=[d.id], request=request)}
                for d in rel]


class OfferReadWithDetailsSerializer(serializers.ModelSerializer):
    """
    READ serializer used for PATCH response only:
    - details as full JSON (not links)
    - includes min_price (int) and min_delivery_time (int)
    - includes user (= business_user_id)
    """
    user = serializers.IntegerField(source="business_user_id", read_only=True)
    details = OfferDetailSerializer(many=True, read_only=True)
    min_price = serializers.IntegerField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Offer
        fields = (
            "id", "user", "title", "image", "description",
            "created_at", "updated_at",
            "details", "min_price", "min_delivery_time",
        )
