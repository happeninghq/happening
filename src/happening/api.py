from django.contrib.auth.models import User
from rest_framework import viewsets
from happening.serializers import UserSerializer


class Api(object):

    """Create an API entry for a model."""

    @classmethod
    def as_viewset(api):
        """Convert the Api into a django_rest_framework viewset."""
        class V(api, viewsets.ModelViewSet):
            def get_queryset(self):
                return api.model.objects.get_for_user(self.request.user)
        V.__name__ = api.__name__[:-3]
        return V


class UserApi(Api):

    """User API."""

    model = User
    serializer_class = UserSerializer
