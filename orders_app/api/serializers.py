from rest_framework import serializers
from ..models import Order
from offers_app.models import OfferDetail


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'customer_user',
            'business_user',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields


class OrderCreateSerializer(serializers.Serializer):
    offer_detail_id = serializers.IntegerField()

    def validate_offer_detail_id(self, value):
        try:
            detail = (
                OfferDetail.objects
                .select_related('offer', 'offer__business_user')
                .get(pk=value)
            )
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError(
                'OfferDetail mit dieser ID existiert nicht.')

        self.context['offer_detail'] = detail
        return value

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        detail = self.context["offer_detail"]
        business_user = getattr(detail, "business_user", None)
        if business_user is None and hasattr(detail, "offer"):
            business_user = detail.offer.business_user

        title = getattr(detail, "title", None)
        if hasattr(detail, "offer") and getattr(detail.offer, "title", None):
            title = detail.offer.title

        order = Order.objects.create(  # Creating order
            customer_user=user,
            business_user=business_user,
            title=title or "",
            revisions=getattr(detail, "revisions", 0),
            delivery_time_in_days=getattr(detail, "delivery_time_in_days", 1),
            price=getattr(detail, "price", 0),
            features=getattr(detail, "features", []) or [],
            offer_type=getattr(detail, "offer_type", Order.OfferType.BASIC),
            status=Order.Status.IN_PROGRESS,
        )
        return order


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """
    For PATCH method only. 'status' is editable.
    """
    class Meta:
        model = Order
        fields = ['status']
