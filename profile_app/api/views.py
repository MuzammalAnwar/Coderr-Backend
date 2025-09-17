from rest_framework.generics import get_object_or_404
from rest_framework.generics import ListAPIView
from .serializers import CustomerProfileSerializer, BusinessProfileSerializer
from auth_app.models import User
from rest_framework import mixins, viewsets
from .permissions import IsProfileOwnerOrReadOnly


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


class ProfileDetailView(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsProfileOwnerOrReadOnly]
    http_method_names = ['get', 'patch', 'head', 'options']

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        user = self.get_object()
        if user.type == User.Usertype.CUSTOMER:
            return CustomerProfileSerializer
        return BusinessProfileSerializer

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)
