"""
Serializers for requests to `favorite` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class FetchFavoritesRequest(serializers.Serializer):
    resource_id = serializers.IntegerField(min_value=1, allow_null=True, default=None)
    user = serializers.EmailField(allow_blank=True, default="")
    page = serializers.IntegerField(min_value=1, allow_null=True, default=None)
    limit = serializers.IntegerField(min_value=1, allow_null=True, default=None)
    top = serializers.IntegerField(min_value=1, allow_null=True, default=None)
