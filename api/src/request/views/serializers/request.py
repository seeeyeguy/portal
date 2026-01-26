"""
Serializers for requests to `Request` views. Serializers provide
validation for request parameters.
"""

# pylint: disable=abstract-method
from rest_framework import serializers

from directory.views.serializers import CreateResourceRequest, UpdateResourceRequest


class CreateRequestRequest(CreateResourceRequest):
    """Request serializer for POST /v1/request/request."""

    stage = serializers.CharField(max_length=10, default="DRAFT")


class UpdateRequestRequest(UpdateResourceRequest, CreateRequestRequest):
    """Request serializer for PUT /v1/request/request."""


class BaseRequestRequestQueryParams(serializers.Serializer):
    """Base Request serializer for PUT and DELETE /v1/request/request query params."""

    id = serializers.IntegerField(min_value=1)


class UpdateRequestRequestQueryParams(BaseRequestRequestQueryParams):
    """Request serializer for PUT /v1/request/request query params."""


class DeleteRequestRequestQueryParams(BaseRequestRequestQueryParams):
    """Request serializer for DELETE /v1/request/request query params."""


class FetchRequestRequest(serializers.Serializer):
    """Request serializer for GET /v1/request/request."""

    id = serializers.IntegerField(allow_null=True, default=None)
    originator = serializers.EmailField(max_length=512, allow_null=True, default=None)
    stages = serializers.ListField(child=serializers.IntegerField(), default=None)
    subfunctions = serializers.ListField(child=serializers.IntegerField(), default=None)
    status = serializers.CharField(max_length=512, allow_null=True, default=None)
    page = serializers.IntegerField(allow_null=True, default=None)
    limit = serializers.IntegerField(allow_null=True, default=None)
    include_archived = serializers.BooleanField(allow_null=True, default=False)
    deleted = serializers.BooleanField(allow_null=True, default=True)
