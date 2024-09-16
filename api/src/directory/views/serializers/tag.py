"""
Serializers for requests to `Tag` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class FetchTagRequest(serializers.Serializer):
    """Request serializer for GET /v1/directory/tags."""

    id = serializers.IntegerField(allow_null=True, default=None)


class TagSearchRequest(serializers.Serializer):
    """Request serializer for GET /v1/directory/tags/search."""

    label = serializers.CharField(max_length=1028)
