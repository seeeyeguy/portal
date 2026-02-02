"""
Serializers for requests to `Content` views. Serializers provide
validation for request parameters.
"""

# pylint: disable=abstract-method
from rest_framework import serializers


class BaseContentRequest(serializers.Serializer):
    """Serializers used for POST and PUT /v1/content/content requests."""

    key = serializers.CharField(max_length=512)
    content = serializers.JSONField()


class CreateContentRequest(BaseContentRequest):
    """Request serializer for POST /v1/content/content."""


class FetchContentRequest(serializers.Serializer):
    """Request serializer for GET /v1/content/content."""

    key = serializers.CharField(max_length=512)


class DeleteContentRequest(serializers.Serializer):
    """Request serializer for DELETE /v1/content/content."""

    key = serializers.CharField(max_length=512)
