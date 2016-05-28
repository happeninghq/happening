from rest_framework import serializers
from django.contrib.auth.models import User
# from happening.configuration import get_configuration_variables,
# attach_to_serializer


class Serializer(serializers.HyperlinkedModelSerializer):
    """Serializer that considers configuration variables."""

    configuration_variables = None

    def __init__(self, *args, **kwargs):
        """Initialise the serializer."""
        super(Serializer, self).__init__(*args, **kwargs)

        # Now we need to get all active plugin fields declared on Events and
        # add them
        # if self.configuration_variables:
        #     variables = get_configuration_variables(
        # self.configuration_variables)
        #     attach_to_serializer(self, variables)


class UserSerializer(Serializer):
    """User API."""

    class Meta:
        model = User
        fields = ('id', 'username')
