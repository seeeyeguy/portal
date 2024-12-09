"""
Serializers for requests to `Tag` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class BasePostTagRequest(serializers.Serializer):
    """Base serializer for POST and PUT /v1/directory/tags requests."""

    label = serializers.CharField(max_length=1028)


class CreateTagRequest(BasePostTagRequest):
    """Request serializer for POST /v1/directory/tags."""


class UpdateTagRequest(BasePostTagRequest):
    """Request serializer for PUT /v1/directory/tags."""


class UpdateTagRequestQueryParams(serializers.Serializer):
    """Request serializer for PUT /v1/directory/tags query params."""

    id = serializers.IntegerField()


class DeleteTagRequest(serializers.Serializer):
    """Request serializer for DELETE /v1/directory/tags."""

    id = serializers.IntegerField()


class FetchTagRequest(serializers.Serializer):
    """Request serializer for GET /v1/directory/tags."""

    id = serializers.IntegerField(allow_null=True, default=None)
    page = serializers.IntegerField(allow_null=True, default=None)
    limit = serializers.IntegerField(allow_null=True, default=None)


class TagSearchRequest(serializers.Serializer):
    """Request serializer for GET /v1/directory/tags/search."""

    label = serializers.CharField(max_length=1028)
