"""
Serializers for `Function` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from directory.models.Function.Function import Function


class FunctionSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Function`."""

    class Meta:
        """Meta for `Function` serializer."""

        model = Function
        fields = "__all__"
