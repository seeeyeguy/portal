"""
Serializers for `Visit` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from analytics.models.Visit.Visit import Visit

from directory.models.Resource.serializers import ResourceSerializer


class VisitSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Visit`."""

    resource = ResourceSerializer(read_only=True)

    class Meta:
        """Meta for `Visit` serializer."""

        model = Visit
        fields = "__all__"
