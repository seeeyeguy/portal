"""
Serializers for `Resource` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from directory.models.Resource.Resource import Resource

from directory.models.EmployeeLevel.serializers import EmployeeLevelSerializer
from directory.models.SubFunction.serializers import SubFunctionSerializer
from directory.models.Tag.serializers import TagSerializer


class ResourceSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Resource`."""

    levels = EmployeeLevelSerializer(many=True, read_only=True)
    subfunctions = SubFunctionSerializer(many=True, read_only=True)
    Tag = TagSerializer(many=True, read_only=True)

    class Meta:
        """Meta for `Resource` serializer."""

        model = Resource
        fields = "__all__"
