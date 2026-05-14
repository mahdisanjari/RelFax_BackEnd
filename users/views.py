from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,UserListSerializer
)
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
User = get_user_model()
from django.core.mail import send_mail

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"detail": "Email confirmed. You can now log in."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid or expired confirmation link."}, status=status.HTTP_400_BAD_REQUEST)
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {"detail": "User created. A confirmation email has been sent."}
        return response

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


class UserListView(generics.ListAPIView):
    """
    list users with search capability
    excluding authenticated user
    """
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter]
    search_fields = ["email", "first_name", "last_name", "bio"]

    def get_queryset(self):
        # exclude authenticated user from the list
        return User.objects.exclude(id=self.request.user.id)

class ResendConfirmationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email, is_active=False)
        except User.DoesNotExist:
            # For security, don't reveal if user exists or is already active
            return Response({"detail": "If the email is registered and inactive, a new confirmation link has been sent."},
                            status=status.HTTP_200_OK)

        # Generate new token and uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_url = f"https://relfax.com/auth/confirm/{uid}/{token}/"

        subject = "Confirm your email address (resend)"
        message = f"Hi {user.email},\n\nPlease click the link below to activate your account:\n\n{confirm_url}"
        send_mail(subject, message, user.email, [user.email])

        return Response({"detail": "Confirmation email sent."}, status=status.HTTP_200_OK)