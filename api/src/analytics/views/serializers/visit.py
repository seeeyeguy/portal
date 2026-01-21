"""
Serializers for requests to `Visit` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class CreateVisitRequest(serializers.Serializer):
    """Request serializer for POST /v1/analytics/visits."""

    resource = serializers.IntegerField(min_value=1)


class FetchVisitRequest(serializers.Serializer):
    """Request serializer for GET /v1/analytics/visits."""

    user = serializers.EmailField(allow_blank=True, default="")
    resource = serializers.IntegerField(min_value=1, allow_null=True, default=None)
    page = serializers.IntegerField(min_value=1, allow_null=True, default=None)
    limit = serializers.IntegerField(min_value=1, allow_null=True, default=None)
    top = serializers.IntegerField(min_value=1, allow_null=True, default=None)
