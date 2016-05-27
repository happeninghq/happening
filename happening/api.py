from django.contrib.auth.models import User
from rest_framework import viewsets
from happening.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """User API."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
