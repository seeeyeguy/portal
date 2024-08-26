"""
Serializers for `Tag` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from directory.models.Tag.Tag import Tag


class TagSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Tag`."""

    class Meta:
        """Meta for `Tag` serializer."""

        model = Tag
        fields = "__all__"
