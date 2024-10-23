"""
Serializers for requests to `Query` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class CreateQueryRequest(serializers.Serializer):
    """Request serializer for POST /v1/analytics/queries."""

    search_term = serializers.CharField(max_length=512)


class FetchQueryRequest(serializers.Serializer):
    """Request serializer for GET /v1/analytics/queries."""

    id = serializers.IntegerField(allow_null=True, default=None)
    user = serializers.EmailField(allow_blank=True, default="")
    page = serializers.IntegerField(allow_null=True, default=None)
    limit = serializers.IntegerField(allow_null=True, default=None)
