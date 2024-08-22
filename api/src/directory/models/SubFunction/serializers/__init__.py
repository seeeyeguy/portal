"""
Serializers for `SubFunction` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from directory.models.SubFunction.SubFunction import SubFunction

from directory.models.Function.serializers import FunctionSerializer


class SubFunctionSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `SubFunction`."""

    function = FunctionSerializer(read_only=True)

    class Meta:
        """Meta for `SubFunction` serializer."""

        model = SubFunction
        fields = "__all__"
