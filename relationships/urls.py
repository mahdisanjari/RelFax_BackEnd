from django.urls import path
from .views import (
    SendRelationshipRequestView,
    RelationshipRequestActionView,
    UserPublicRelationshipsView
)

urlpatterns = [
    path("request/", SendRelationshipRequestView.as_view()),
    path("request/<int:pk>/action/", RelationshipRequestActionView.as_view()),
    path("user/<int:user_id>/relationships/", UserPublicRelationshipsView.as_view()),
]

