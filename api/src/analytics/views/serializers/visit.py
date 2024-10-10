"""
Serializers for requests to `Visit` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class CreateVisitRequest(serializers.Serializer):
    """Request serializer for POST /v1/analytics/visits."""

    user = serializers.EmailField()
    resource = serializers.IntegerField()


class FetchVisitRequest(serializers.Serializer):
    """Request serializer for GET /v1/analytics/visits."""

    id = serializers.IntegerField(allow_null=True, default=None)
    user = serializers.EmailField(allow_blank=True, default="")
    resource = serializers.IntegerField(allow_null=True, default=None)
    page = serializers.IntegerField(allow_null=True, default=None)
    limit = serializers.IntegerField(allow_null=True, default=None)
