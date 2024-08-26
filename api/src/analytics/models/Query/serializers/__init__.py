"""
Serializers for `Query` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from analytics.models.Query.Query import Query

from directory.models.Resource.serializers import ResourceSerializer
from users.models.User.serializers import UserSerializer


class QuerySerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Query`."""

    user = UserSerializer(read_only=True)
    resources = ResourceSerializer(many=True, read_only=True)

    class Meta:
        """Meta for `Query` serializer."""

        model = Query
        fields = "__all__"
