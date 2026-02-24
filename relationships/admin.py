from django.contrib import admin
from .models import RelationshipType, RelationshipRequest, Relationship

admin.site.register(RelationshipType)
admin.site.register(RelationshipRequest)
admin.site.register(Relationship)
