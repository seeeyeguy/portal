"""
Serializers for requests to `Query` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class CreateQueryRequest(serializers.Serializer):
    """Request serializer for POST /v1/analytics/queries."""

    user = serializers.EmailField()
    search_term = serializers.CharField(max_length=512)
