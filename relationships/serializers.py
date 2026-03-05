from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import RelationshipRequest, Relationship, RelationshipType

User = get_user_model()


User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    """Used for embedding user info inside relationship requests"""

    class Meta:
        model = User
        fields = ["id", "email"]


class RelationshipRequestListSerializer(serializers.ModelSerializer):
    from_user = SimpleUserSerializer()
    to_user = SimpleUserSerializer()
    relationship_type_name = serializers.CharField(source="relationship_type.name")

    class Meta:
        model = RelationshipRequest
        fields = [
            "id",
            "from_user",
            "to_user",
            "relationship_type_name",
            "status",
            "created_at",
        ]
class RelationshipTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationshipType
        fields = ["id", "name", "is_public"]


class RelationshipRequestCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RelationshipRequest
        fields = ["to_user", "relationship_type"]

    def validate(self, data):
        request = self.context["request"]
        from_user = request.user
        to_user = data["to_user"]

        if from_user == to_user:
            raise serializers.ValidationError("You cannot send request to yourself.")

        if RelationshipRequest.objects.filter(
            from_user=from_user,
            to_user=to_user,
            status="pending"
        ).exists():
            raise serializers.ValidationError("Request already sent.")

        return data

    def create(self, validated_data):
        return RelationshipRequest.objects.create(
            from_user=self.context["request"].user,
            **validated_data
        )

class RelationshipRequestActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["accept", "reject"])


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = "__all__"

class RelationshipRequestSerializer(serializers.ModelSerializer):
    from_user_username = serializers.CharField(source='from_user.username', read_only=True)
    from_user_full_name = serializers.SerializerMethodField()
    relationship_type_name = serializers.CharField(source='relationship_type.name', read_only=True)

    class Meta:
        model = RelationshipRequest
        fields = [
            'id',
            'from_user',
            'from_user_username',
            'from_user_full_name',
            'to_user',
            'relationship_type',
            'relationship_type_name',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_from_user_full_name(self, obj):
        user = obj.from_user
        return f"{user.first_name} {user.last_name}".strip()