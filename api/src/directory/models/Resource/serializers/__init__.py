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

    employee_levels = EmployeeLevelSerializer(many=True, read_only=True)
    subfunctions = SubFunctionSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    primary_point_of_contact = serializers.CharField(
        source="requests.originator.user.email"
    )

    class Meta:
        """Meta for `Resource` serializer."""

        model = Resource
        fields = "__all__"
