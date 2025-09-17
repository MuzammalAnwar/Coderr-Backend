from django.urls import path, include
from .views import CustomerProfilesListView, BusinessProfilesListView, ProfileDetailView

profile_detail = ProfileDetailView.as_view({
    "get": "retrieve",
    "patch": "update",
})

urlpatterns = [
    path(
        'profiles/customer/',
        CustomerProfilesListView.as_view(),
        name='customer-profile-list'
    ),
    path(
        'profiles/business/',
        BusinessProfilesListView.as_view(),
        name='business-profile-list'
    ),
    path(
        'profile/<int:pk>/',
        profile_detail,
        name='profile-detail-view'
    )
]
