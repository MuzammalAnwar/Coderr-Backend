from rest_framework.generics import ListAPIView
from .serializers import CustomerProfileSerializer, BusinessProfileSerializer
from auth_app.models import User


class CustomerProfilesListView(ListAPIView):
    serializer_class = CustomerProfileSerializer

    def get_queryset(self):
        qs = User.objects.filter(type='customer')
        return qs.distinct()


class BusinessProfilesListView(ListAPIView):
    serializer_class = BusinessProfileSerializer

    def get_queryset(self):
        qs = User.objects.filter(type='business')
        return qs.distinct()
