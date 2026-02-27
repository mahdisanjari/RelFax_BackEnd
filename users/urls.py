from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    MyProfileView,
    EditProfileView,
    PublicProfileView
)
from .views import UserListView
urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("me/", MyProfileView.as_view()),
    path("me/edit/", EditProfileView.as_view()),
    path("profile/<int:id>/", PublicProfileView.as_view()),
    path("list/", UserListView.as_view()),
]