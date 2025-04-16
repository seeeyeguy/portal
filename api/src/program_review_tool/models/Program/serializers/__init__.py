"""
Serializers for `Program` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from program_review_tool.models.Program import Program


class ProgramSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Program`."""

    segment = serializers.CharField(source="segment.name", default="")

    class Meta:
        """Meta for `Program` serializer."""

        model = Program
        fields = "__all__"
