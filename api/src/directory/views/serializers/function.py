"""
Serializers for requests to `Function` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class FetchFunctionRequest(serializers.Serializer):
    """Request serializer for GET /v1/directory/functions."""

    id = serializers.IntegerField(allow_null=True, default=None)
