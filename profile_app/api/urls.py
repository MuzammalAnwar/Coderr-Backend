from django.urls import path, include
from .views import CustomerProfilesListView, BusinessProfilesListView


urlpatterns = [
    path('profiles/customer/', CustomerProfilesListView.as_view(), name='customer-profile-list'),
    path('profiles/business/', BusinessProfilesListView.as_view(), name='business-profile-list')
]