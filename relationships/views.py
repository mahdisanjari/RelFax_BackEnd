from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import RelationshipRequest, Relationship
from .serializers import (
    RelationshipRequestCreateSerializer,
    RelationshipRequestActionSerializer,
    RelationshipSerializer
)


class SendRelationshipRequestView(generics.CreateAPIView):
    """
    send a relationship request to another user.

    POST parameters:
    - to_user: integer (user id)
    - relationship_type: integer (relationship type id)
    """
    serializer_class = RelationshipRequestCreateSerializer
    permission_classes = [IsAuthenticated]


class RelationshipRequestActionView(generics.GenericAPIView):
    serializer_class = RelationshipRequestActionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        relation_request = get_object_or_404(
            RelationshipRequest,
            pk=pk,
            to_user=request.user,
            status="pending"
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = serializer.validated_data["action"]

        with transaction.atomic():

            if action == "accept":
                relation_request.status = "accepted"
                relation_request.save()

                Relationship.objects.create(
                    user1=relation_request.from_user,
                    user2=relation_request.to_user,
                    relationship_type=relation_request.relationship_type
                )

            elif action == "reject":
                relation_request.status = "rejected"
                relation_request.save()

        return Response({"detail": f"Request {action}ed successfully"})


class RelationshipRequestActionView(generics.GenericAPIView):
    serializer_class = RelationshipRequestActionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        relation_request = get_object_or_404(
            RelationshipRequest,
            pk=pk,
            to_user=request.user,
            status="pending"
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        action = serializer.validated_data["action"]

        with transaction.atomic():

            if action == "accept":
                relation_request.status = "accepted"
                relation_request.save()

                Relationship.objects.create(
                    user1=relation_request.from_user,
                    user2=relation_request.to_user,
                    relationship_type=relation_request.relationship_type
                )

            elif action == "reject":
                relation_request.status = "rejected"
                relation_request.save()

        return Response({"detail": f"Request {action}ed successfully"})

from django.db.models import Q

class UserPublicRelationshipsView(generics.ListAPIView):
    serializer_class = RelationshipSerializer
    permission_classes = []

    def get_queryset(self):
        user_id = self.kwargs["user_id"]

        return Relationship.objects.filter(
            Q(user1_id=user_id) | Q(user2_id=user_id),
            is_active=True,
            relationship_type__is_public=True
        )
