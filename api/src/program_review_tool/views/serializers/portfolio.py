"""
Serializers for requests to `Portfolio` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class BaseMutationPortfolioRequest(serializers.Serializer):
    """Base serializer for /v1/program-review-tool/portfolio mutation requests."""

    name = serializers.CharField(max_length=512)
    programs = serializers.ListField(child=serializers.IntegerField())


class CreatePortfolioRequest(BaseMutationPortfolioRequest):
    """Request serializer for POST /v1/program-review-tool/portfolio."""


class UpdatePortfolioRequest(BaseMutationPortfolioRequest):
    """Request serializer for PUT /v1/program-review-tool/portfolio."""


class UpdatePortfolioRequestQueryParams(serializers.Serializer):
    """Request serializer for PUT /v1/program-review-tool/portfolio query params."""

    id = serializers.IntegerField()


class DeletePortfolioRequestQueryParams(serializers.Serializer):
    """Request serializer for DELETE /v1/program-review-tool/portfolio query params."""

    id = serializers.IntegerField()


class FetchPortfolioRequestQueryParams(serializers.Serializer):
    """Request serializer for GET /v1/program-review-tool/portfolio query params."""

    user = serializers.CharField(max_length=512)
