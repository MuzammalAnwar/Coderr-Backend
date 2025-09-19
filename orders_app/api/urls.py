from django.urls import path
from .views import OrdersListCreateView, OrderDetailView, OrderCountView, CompletedOrderCountView

urlpatterns = [
    path(
        'orders/',
        OrdersListCreateView.as_view(),
        name='orders-list-create-view'
    ),
    path(
        'orders/<int:pk>/',
        OrderDetailView.as_view(),
        name='orders-detail-view'
    ),
    path(
        'order-count/<int:business_user_id>/',
        OrderCountView.as_view(),
        name='order-count'
    ),
    path(
        'completed-order-count/<int:business_user_id>/',
        CompletedOrderCountView.as_view(),
        name='completed-order-count'
    ),
]
