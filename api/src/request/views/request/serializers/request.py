"""
Serializers for requests to `Request` views. Serializers provide
validation for request parameters.
"""

# pylint: disable=abstract-method
from rest_framework import serializers

from directory.views.serializers import CreateResourceRequest, UpdateResourceRequest


class CreateRequestRequest(CreateResourceRequest):
    """Request serializer for POST /v1/request/request."""

    stage = serializers.IntegerField(min_value=1, max_value=100)


class UpdateRequestRequest(UpdateResourceRequest, CreateRequestRequest):
    """Request serializer for PUT /v1/request/request."""


class UpdateRequestRequestQueryParams(serializers.Serializer):
    """Request serializer for PUT /v1/request/request query params."""

    id = serializers.IntegerField(min_value=1)


class FetchRequestRequest(serializers.Serializer):
    """Request serializer for GET /v1/request/request."""

    id = serializers.IntegerField(allow_null=True, default=None)
    originator = serializers.CharField(max_length=512, allow_null=True, default=None)
    stage = serializers.IntegerField(allow_null=True, default=None)
    status = serializers.CharField(max_length=512, allow_null=True, default=None)
    page = serializers.IntegerField(allow_null=True, default=None)
    limit = serializers.IntegerField(allow_null=True, default=None)
    include_archived = serializers.BooleanField(allow_null=True, default=False)
