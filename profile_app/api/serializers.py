from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import get_user_model, authenticate
from auth_app.models import User


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='id', queryset=User.objects.all())

    class Meta:
        model = User
        fields = [
            'user',
            'username',
            'first_name',
            'last_name',
            'file',
            'uploaded_at',
            'type'
        ]


class BusinessProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source='id', queryset=User.objects.all())

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
            'type'
        ]
