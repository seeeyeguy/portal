"""
Serializers for requests to `Program` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class FetchProgramRequestQueryParams(serializers.Serializer):
    """Request serializer for GET /v1/program-review-tool/program query params."""

    ids = serializers.ListField(child=serializers.IntegerField())


class ReviewProgramRequest(serializers.Serializer):
    """Request serializer for POST /v1/program-review-tool/program/review."""

    programs = serializers.ListField(child=serializers.IntegerField())
    review_name = serializers.CharField(max_length=1028)
