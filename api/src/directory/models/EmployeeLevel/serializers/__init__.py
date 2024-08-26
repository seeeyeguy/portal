"""
Serializers for `EmployeeLevel` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from directory.models.EmployeeLevel.EmployeeLevel import EmployeeLevel


class EmployeeLevelSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `EmployeeLevel`."""

    class Meta:
        """Meta for `EmployeeLevel` serializer."""

        model = EmployeeLevel
        fields = "__all__"
