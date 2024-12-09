"""
Serializers for requests to `SubFunction` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class BasePostSubFunctionRequest(serializers.Serializer):
    """Base serializer for POST and PUT /v1/directory/subfunctions requests."""

    name = serializers.CharField(max_length=512)
    description = serializers.CharField(max_length=8192)
    function = serializers.IntegerField()


class CreateSubFunctionRequest(BasePostSubFunctionRequest):
    """Request serializer for POST /v1/directory/subfunctions."""


class UpdateSubFunctionRequest(BasePostSubFunctionRequest):
    """Request serializer for PUT /v1/directory/subfunctions."""


class UpdateSubFunctionRequestQueryParams(serializers.Serializer):
    """Request serializer for PUT /v1/directory/subfunctions query params."""

    id = serializers.IntegerField()


class DeleteSubFunctionRequest(serializers.Serializer):
    """Request serializer for DELETE /v1/directory/subfunctions."""

    id = serializers.IntegerField()


class FetchSubFunctionRequest(serializers.Serializer):
    """Request serializer for GET /v1/directory/subfunctions."""

    id = serializers.IntegerField(allow_null=True, default=None)
