"""
Serializers for `Segment` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from users.models import Segment


class SegmentSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Segment`."""

    class Meta:
        """Meta for `Segment` serializer."""

        model = Segment
        fields = "__all__"
