"""
Serializers for `Usage` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from program_review_tool.models.Usage import Usage


class UsageSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Usage`."""

    class Meta:
        """Meta for `Usage` serializer."""

        model = Usage
        fields = "__all__"
