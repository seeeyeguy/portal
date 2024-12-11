"""
Serializers for requests to `EmployeeLevel` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class BasePostEmployeeLevelRequest(serializers.Serializer):
    """Base serializer for POST and PUT /v1/directory/employee-levels requests."""

    name = serializers.CharField(max_length=512)
    description = serializers.CharField(max_length=8192)


class CreateEmployeeLevelRequest(BasePostEmployeeLevelRequest):
    """Request serializer for POST /v1/directory/employee-levels."""


class UpdateEmployeeLevelRequest(BasePostEmployeeLevelRequest):
    """Request serializer for PUT /v1/directory/employee-levels."""


class UpdateEmployeeLevelRequestQueryParams(serializers.Serializer):
    """Request serializer for PUT /v1/directory/employee-levels query params."""

    id = serializers.IntegerField()


class DeleteEmployeeLevelRequest(serializers.Serializer):
    """Request serializer for DELETE /v1/directory/employee-levels."""

    id = serializers.IntegerField()


class FetchEmployeeLevelRequest(serializers.Serializer):
    """Request serializer for GET /v1/directory/employee-levels."""

    id = serializers.IntegerField(allow_null=True, default=None)
