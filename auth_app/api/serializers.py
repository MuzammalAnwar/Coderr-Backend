from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password', 'type']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        username = self.validated_data['username']
        if pw != repeated_pw:
            raise serializers.ValidationError("Passwords do not match")
        names = username.strip().split(" ", 1)
        username = username.replace(" ", "_")
        account = User(
            username=username,
            email=self.validated_data['email'],
            type=self.validated_data['type']
        )
        account.set_password(pw)
        account.save()
        return account


class LoginSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with given username does not exist")
        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=user.username,
                password=password
            )
            if not user:
                raise serializers.ValidationError('Invalid password')
        attrs['user'] = user
        return attrs
