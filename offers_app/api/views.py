from django.db.models import Min
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from offers_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferListItemSerializer, OfferDetailSerializer, OfferReadSerializer, OfferReadWithDetailsSerializer
from .permissions import IsBusinessForWrite, IsOfferOwnerOrReadOnly
from .pagination import DefaultPageNumberPagination
from django.db.models.functions import Cast
from django.db.models import Min, IntegerField
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from decimal import Decimal, InvalidOperation


class OfferDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,
                          IsBusinessForWrite, IsOfferOwnerOrReadOnly]

    def get_queryset(self):
        return (
            Offer.objects
            .select_related("business_user")
            .prefetch_related("details")
            .annotate(
                min_price=Cast(Min("details__price"), IntegerField()),
                min_delivery_time=Min("details__delivery_time_in_days"),
            )
        )

    def get_serializer_class(self):
        return OfferReadSerializer if self.request.method == "GET" else OfferSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    """Validate with write serializer, then return full details JSON."""

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        write_ser = OfferSerializer(
            instance, data=request.data, partial=partial, context=self.get_serializer_context()
        )
        write_ser.is_valid(raise_exception=True)
        self.perform_update(write_ser)

        obj = self.get_queryset().get(pk=instance.pk)
        read_ser = OfferReadWithDetailsSerializer(
            obj, context=self.get_serializer_context())
        return Response(read_ser.data)


class OfferListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsBusinessForWrite]
    pagination_class = DefaultPageNumberPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['-updated_at']

    def get_queryset(self):
        qs = (
            Offer.objects
            .select_related('business_user')
            .prefetch_related('details')
            .annotate(
                min_price=Min('details__price'),                     
                min_delivery_time=Min('details__delivery_time_in_days')
            )
        )

        # creator_id (integer pnly)
        creator_id = self.request.query_params.get('creator_id')
        if creator_id is not None and creator_id != '':
            creator_id = self._parse_non_negative_int(creator_id, 'creator_id')
            qs = qs.filter(business_user_id=creator_id)

        # min_price (integer only)
        min_price = self.request.query_params.get('min_price')
        if min_price is not None and min_price != '':
            min_price = self._parse_non_negative_decimal(
                min_price, 'min_price')
            qs = qs.filter(min_price__gte=min_price)

        # max_delivery_time (integer only)
        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time is not None and max_delivery_time != '':
            max_delivery_time = self._parse_non_negative_int(
                max_delivery_time, 'max_delivery_time')
            qs = qs.filter(min_delivery_time__lte=max_delivery_time)

        return qs

    def _parse_non_negative_int(self, raw, field_name):
        try:
            value = int(raw)
        except (TypeError, ValueError):
            raise ValidationError({field_name: 'Must be an integer.'})
        if value < 0:
            raise ValidationError({field_name: 'Must be >= 0.'})
        return value

    def _parse_non_negative_decimal(self, raw, field_name):
        try:
            value = Decimal(str(raw))
        except (InvalidOperation, TypeError, ValueError):
            raise ValidationError({field_name: 'Must be a number.'})
        if value < 0:
            raise ValidationError({field_name: 'Must be >= 0.'})
        return value


class OfferRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OfferListItemSerializer

    def get_queryset(self):
        return (
            Offer.objects
            .select_related("business_user")
            .prefetch_related("details")
            .annotate(
                min_price=Min("details__price"),
                min_delivery_time=Min("details__delivery_time_in_days"),
            )
        )


class OfferDetailRetrieveView(RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    lookup_field = "pk"
