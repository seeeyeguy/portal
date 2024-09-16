"""
Serializers for requests to `SubFunction` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class FetchSubFunctionRequest(serializers.Serializer):
    """Request serializer for GET /v1/directory/subfunctions."""

    id = serializers.IntegerField(allow_null=True, default=None)
