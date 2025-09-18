from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework import permissions, status
from orders_app.models import Order



class OrdersListCreateView(ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()