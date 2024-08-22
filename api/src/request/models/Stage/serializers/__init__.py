"""
Serializers for `Stage` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from request.models.Stage.Stage import Stage


class StageSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Stage`."""

    class Meta:
        """Meta for `Stage` serializer."""

        model = Stage
        fields = "__all__"
