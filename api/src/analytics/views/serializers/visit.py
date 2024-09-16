"""
Serializers for requests to `Visit` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class CreateVisitRequest(serializers.Serializer):
    """Request serializer for POST /v1/analytics/visits."""

    user = serializers.EmailField()
    resource = serializers.IntegerField()
