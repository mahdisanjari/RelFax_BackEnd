from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class RelationshipType(models.Model):
    name = models.CharField(max_length=50)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class RelationshipRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    from_user = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    relationship_type = models.ForeignKey(RelationshipType, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)


class Relationship(models.Model):
    user1 = models.ForeignKey(User, related_name="relationships_from", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="relationships_to", on_delete=models.CASCADE)
    relationship_type = models.ForeignKey(RelationshipType, on_delete=models.CASCADE)

    started_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user1", "user2", "relationship_type")
