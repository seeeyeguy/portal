"""
Serializers for requests to `Usage` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class FetchUsageRequest(serializers.Serializer):
    """Request serializer for GET /v1/analytics/usage."""

    id = serializers.IntegerField(min_value=1, allow_null=True, default=None)
    user = serializers.EmailField(allow_blank=True, default="")
    page = serializers.IntegerField(min_value=1, allow_null=True, default=None)
    limit = serializers.IntegerField(min_value=1, allow_null=True, default=None)
    pa_number = serializers.CharField(allow_blank=True, default=None)
    success = serializers.BooleanField(allow_null=True, default=None)
