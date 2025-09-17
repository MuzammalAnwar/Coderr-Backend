from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from auth_app.models import User
from rest_framework.generics import ListAPIView


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id', read_only=True)
    username = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'uploaded_at',
            'type',
        ]
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def get_fields(self):
        fields = super().get_fields()
        view = self.context.get('view')
        if view and not isinstance(view, ListAPIView):
            fields['email'] = serializers.EmailField(read_only=False)
            fields['created_at'] = serializers.DateTimeField(read_only=True)
        return fields


class BusinessProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = User
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'location',
            'tel',
            'description',
            'working_hours',
            'type',
        ]
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def get_fields(self):
        fields = super().get_fields()
        view = self.context.get('view')
        if view and not isinstance(view, ListAPIView):
            fields['email'] = serializers.EmailField(read_only=False)
            fields['created_at'] = serializers.DateTimeField(read_only=True)
        return fields
