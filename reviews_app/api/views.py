from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from ..models import Review
from .permissions import IsAuthenticatedReadOnly, IsCustomer, IsReviewOwner
from .serializers import ReviewSerializer, ReviewCreateSerializer,   ReviewUpdateSerializer


class ReviewListCreateView(ListCreateAPIView):
    """
    /api/reviews/
    GET
    POST
    """
    queryset = Review.objects.select_related("business_user", "reviewer")
    permission_classes = [IsAuthenticatedReadOnly, IsCustomer]

    def get_serializer_class(self):
        return ReviewCreateSerializer if self.request.method == "POST" else ReviewSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        bu_id = self.request.query_params.get("business_user_id")
        rev_id = self.request.query_params.get("reviewer_id")
        ordering = self.request.query_params.get("ordering")

        if bu_id:
            qs = qs.filter(business_user_id=bu_id)
        if rev_id:
            qs = qs.filter(reviewer_id=rev_id)

        allowed = {"updated_at", "rating", "-updated_at", "-rating"}
        if ordering in allowed:
            qs = qs.order_by(ordering)

        return qs

    def create(self, request, *args, **kwargs):
        ser_in = ReviewCreateSerializer(
            data=request.data, context={"request": request})
        ser_in.is_valid(raise_exception=True)
        review = ser_in.save(reviewer=request.user)
        ser_out = ReviewSerializer(review, context={"request": request})
        return Response(ser_out.data, status=status.HTTP_201_CREATED)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    """
    /api/reviews/{id}/
    GET anyone authenticated
    PATCH owner only, rating/description only
    DELETE owner only
    """
    queryset = Review.objects.select_related("business_user", "reviewer")
    permission_classes = [IsAuthenticatedReadOnly, IsReviewOwner]

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return ReviewUpdateSerializer
        return ReviewSerializer

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)

        ser_in = self.get_serializer(instance, data=request.data, partial=True)
        ser_in.is_valid(raise_exception=True)
        self.perform_update(ser_in)

        # respond with the full review object
        ser_out = ReviewSerializer(instance)
        return Response(ser_out.data, status=status.HTTP_200_OK)
