from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer
from rest_framework.response import Response
from django.http import Http404
from rest_framework import permissions, status
from orders_app.models import Order
from .permissions import IsAuthenticatedAndCustomerForCreate, IsOrderBusinessUser
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class OrdersListCreateView(ListCreateAPIView):
    """
    GET  /api/orders/        lists orders where the requesting usere is customer OR business
    POST /api/orders/        create order from offer_detail_id, only permitted for customer acc
    """
    permission_classes = [IsAuthenticatedAndCustomerForCreate]
    queryset = Order.objects.all().order_by("-updated_at")

    def get_queryset(self):
        user = self.request.user
        # Only orders involving the current user
        return Order.objects.filter(
            Q(customer_user=user) | Q(business_user=user)
        ).order_by("-updated_at")

    def get_serializer_class(self):
        return OrderCreateSerializer if self.request.method == "POST" else OrderSerializer

    def create(self, request, *args, **kwargs):
        ser_in = OrderCreateSerializer(
            data=request.data, context={"request": request})
        ser_in.is_valid(raise_exception=True)
        order = ser_in.save()

        ser_out = OrderSerializer(order, context={"request": request})
        return Response(ser_out.data, status=status.HTTP_201_CREATED)


class OrderDetailView(RetrieveUpdateDestroyAPIView):
    """
    PATCH /api/orders/{id}/ for business_users only. updates 'status' field
    DELETE /api/orders/{id}/ only allowed for staff/admin
    """
    queryset = Order.objects.all()
    http_method_names = ['patch', 'delete']

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsOrderBusinessUser()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        return OrderStatusUpdateSerializer

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        self.check_object_permissions(request, order)

        ser_in = self.get_serializer(order, data=request.data, partial=True)
        ser_in.is_valid(raise_exception=True)
        self.perform_update(ser_in)

        ser_out = OrderSerializer(order)
        return Response(ser_out.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        self.check_object_permissions(request, order)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderCountView(APIView):
    """
    GET /api/order-count/<business_user_id>/
    -> {"order_count": <int>}
    Counts orders with status 'in_progress' for the given business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        # 404 if user doesn't exist OR is not a business
        try:
            user = User.objects.get(pk=business_user_id, type='business')
        except User.DoesNotExist:
            raise Http404('Kein Geschäftsbenutzer mit dieser ID gefunden.')

        count = Order.objects.filter(
            business_user_id=user.id,
            status=Order.Status.IN_PROGRESS,
        ).count()
        return Response({'order_count': count})


class CompletedOrderCountView(APIView):
    """
    GET /api/completed-order-count/<business_user_id>/
    Counts orders with status 'completed' for a given business user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            user = User.objects.get(pk=business_user_id, type='business')
        except User.DoesNotExist:
            raise Http404('Kein Geschäftsbenutzer mit dieser ID gefunden.')

        count = Order.objects.filter(
            business_user_id=user.id,
            status=Order.Status.COMPLETED,
        ).count()
        return Response({'completed_order_count': count})
