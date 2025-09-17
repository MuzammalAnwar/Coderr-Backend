from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        allowed_fields = {
            'username',
            'email',
            'password',
            'repeated_password',
            'type'
        }
        received_fields = set(request.data.keys())
        extra_fields = received_fields - allowed_fields
        if extra_fields:
            return Response(
                {"error": f"Invalid fields in request: {', '.join(extra_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id,
                'token': token.key
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'username': user.username,
            'email': user.email,
            'user_id': user.id,
            'token': token.key
        }
        return Response(data)
