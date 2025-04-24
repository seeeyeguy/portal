"""
Serializers for requests to `Disposition` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class CreateDispositionRequest(serializers.Serializer):
    """Request serializer for POST /v1/request/disposition."""

    resource_id = serializers.IntegerField(min_value=1)
    disposition = serializers.CharField(min_length=6, max_length=8)
    justification = serializers.CharField(allow_blank=True)
