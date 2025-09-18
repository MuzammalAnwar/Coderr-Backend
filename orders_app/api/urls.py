from django.urls import path
from .views import OrdersListCreateView

urlpatterns = [
    path(
        'orders/',
        OrdersListCreateView.as_view(),
        name='orders-list-create-view'
    )
    # path('orders/<int:pk>/', ),
    # path('orders/order-count/<int:business_user_id>/', ),
    # path('orders/completed-order-count/<int:business_user_id>/', ),
]
