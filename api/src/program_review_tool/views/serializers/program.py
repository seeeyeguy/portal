"""
Serializers for requests to `Program` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class FetchProgramRequestQueryParams(serializers.Serializer):
    """Request serializer for GET /v1/program-review-tool/program query params."""

    ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, default=[]
    )
    page = serializers.IntegerField(allow_null=True, default=None)
    limit = serializers.IntegerField(allow_null=True, default=None)


class ReviewProgramRequest(serializers.Serializer):
    """Request serializer for POST /v1/program-review-tool/program/review."""

    programs = serializers.ListField(child=serializers.IntegerField())
    review_name = serializers.CharField(max_length=1028)
