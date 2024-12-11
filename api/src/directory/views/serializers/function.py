"""
Serializers for requests to `Function` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class BasePostFunctionRequest(serializers.Serializer):
    """Base serializer for POST and PUT /v1/directory/functions requests."""

    name = serializers.CharField(max_length=512)
    description = serializers.CharField(max_length=8192)


class CreateFunctionRequest(BasePostFunctionRequest):
    """Request serializer for POST /v1/directory/functions."""


class UpdateFunctionRequest(BasePostFunctionRequest):
    """Request serializer for PUT /v1/directory/functions."""


class UpdateFunctionRequestQueryParams(serializers.Serializer):
    """Request serializer for PUT /v1/directory/functions query params."""

    id = serializers.IntegerField()


class DeleteFunctionRequest(serializers.Serializer):
    """Request serializer for DELETE /v1/directory/functions."""

    id = serializers.IntegerField()


class FetchFunctionRequest(serializers.Serializer):
    """Request serializer for GET /v1/directory/functions."""

    id = serializers.IntegerField(allow_null=True, default=None)
