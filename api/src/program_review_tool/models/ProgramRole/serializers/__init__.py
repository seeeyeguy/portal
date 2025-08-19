"""
Serializers for `ProgramRole` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from program_review_tool.models.ProgramRole import ProgramRole


class ProgramRoleSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `ProgramRole`."""

    class Meta:
        """Meta for `ProgramRole` serializer."""

        model = ProgramRole
        fields = "__all__"
