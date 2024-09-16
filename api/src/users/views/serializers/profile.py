"""
Serializers for requests to `Profile` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class FetchProfileRequest(serializers.Serializer):
    """Request serializer for GET /v1/users/profile."""

    user = serializers.EmailField()
