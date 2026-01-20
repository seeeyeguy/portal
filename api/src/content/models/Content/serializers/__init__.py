"""
Serializers for `Content` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from content.models.Content.Content import Content


class ContentSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Content`."""

    class Meta:
        """Meta for `Content` serializer."""

        model = Content
        fields = "__all__"
