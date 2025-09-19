from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg
from reviews_app.models import Review
from offers_app.models import Offer

User = get_user_model()


class BaseInfoView(APIView):
    """
    GET /api/base-info/
    No auth required.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        review_count = Review.objects.count()
        avg_val = Review.objects.aggregate(avg=Avg('rating'))['avg']
        average_rating = round(avg_val or 0.0, 1)
        business_profile_count = User.objects.filter(type='business').count()
        offer_count = Offer.objects.count()

        data = {
            'review_count': review_count,
            'average_rating': average_rating,
            'business_profile_count': business_profile_count,
            'offer_count': offer_count,
        }
        return Response(data)
