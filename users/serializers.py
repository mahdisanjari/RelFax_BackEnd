from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger(__name__)
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "confirm_password"]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )
        user.is_active = False
        user.save()

        try:
            self._send_confirmation_email(user)
        except Exception as e:
            logger.error(f"Confirmation email failed for {user.email}: {e}")
            # If email fails, you might want to delete the user to avoid inactive accounts
            user.delete()
            raise serializers.ValidationError("Unable to send confirmation email. Please try again later.")

        return user

    def _send_confirmation_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_url = f"https://relfax.ca/auth/confirm/{uid}/{token}/"  # adjust URL
        subject = "Confirm your email address"
        message = f"Hi {user.email},\n\nPlease click the link to activate your account:\n\n{confirm_url}"
        send_mail(subject, message, user.email,[user.email])
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            email=data["email"],
            password=data["password"]
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "bio", "profile_status"]
        read_only_fields = ["email"]


class UserListSerializer(serializers.ModelSerializer):
    """Serializer used for listing users"""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "bio",
            'profile_status',
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
#test