from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    register a new user using email and password
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


from rest_framework.views import APIView


class LoginView(APIView):
    """
    login user and return JWT tokens
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class MyProfileView(generics.RetrieveAPIView):
    """
    get authenticated user's profile
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class EditProfileView(generics.UpdateAPIView):
    """
    update authenticated user's profile
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PublicProfileView(generics.RetrieveAPIView):
    """
    get public profile of another user
    """
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    lookup_field = "id"