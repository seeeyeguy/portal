"""
Serializers for requests to `Favorite` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class FavoriteBaseRequestById(serializers.Serializer):
    """Base serializer for a `Favorite` request by id."""

    id = serializers.IntegerField()


class FavoriteBaseRequestByUser(serializers.Serializer):
    """Base serializer for a `Favorite` request by user."""

    user = serializers.EmailField()


class CreateFavoriteRequest(FavoriteBaseRequestByUser):
    """Request serializer for POST /v1/preferences/favorites."""

    resource = serializers.IntegerField()


class RankFavoriteRequest(FavoriteBaseRequestById):
    """Request serializer for PUT /v1/preferences/favorites."""

    rank = serializers.IntegerField()


class RankFavoriteQueryParams(FavoriteBaseRequestByUser):
    """Request serializer for PUT /v1/preferences/favorites query params."""


class DeleteFavoriteRequest(FavoriteBaseRequestById):
    """Request serializer for DELETE /v1/preferences/favorites."""


class FetchFavoriteRequest(FavoriteBaseRequestByUser):
    """Request serializer for GET /v1/preferences/favorites."""
