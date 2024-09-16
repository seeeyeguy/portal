"""
Serializers for requests to `EmployeeLevel` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class FetchEmployeeLevelRequest(serializers.Serializer):
    """Request serializer for GET /v1/directory/employee-levels."""

    id = serializers.IntegerField(allow_null=True, default=None)
