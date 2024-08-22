"""
Serializers for `Request` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from request.models.Request.Request import Request

from directory.models.Resource.serializers import ResourceSerializer
from users.models.Access.serializers import AccessSerializer


class RequestSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Request`."""

    resource = ResourceSerializer(read_only=True)
    originator = AccessSerializer(read_only=True)

    class Meta:
        """Meta for `Request` serializer."""

        model = Request
        fields = "__all__"
