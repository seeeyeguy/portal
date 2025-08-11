"""
Serializers for requests to `Access` and `AccessControl` views.
Serializers provide validation for request parameters.
"""

# pylint: disable=abstract-method
from rest_framework import serializers


class CreateAccessRequest(serializers.Serializer):
    """Request serializer for POST /v1/users/access."""

    user = serializers.EmailField()
    role_level = serializers.IntegerField(min_value=1)
    subfunctions = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, default=[]
    )
    stage_levels = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, default=[]
    )


class RevokeAccessRequestQueryParams(serializers.Serializer):
    """Request serializer for PUT /v1/users/access query params."""

    id = serializers.IntegerField(min_value=1)


class FetchAccessRequest(serializers.Serializer):
    """Request serializer for GET /v1/users/access."""

    id = serializers.IntegerField(allow_null=True, default=None)
    user = serializers.EmailField(allow_null=True, default=None)
    role_levels = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, default=[]
    )
    subfunctions = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, default=[]
    )
    include_revoked = serializers.BooleanField(allow_null=True, default=False)


class UpdateAccessRequest(serializers.Serializer):
    """Request serializer for PUT /v1/users/access/subfunctions."""

    subfunctions = serializers.ListField(child=serializers.IntegerField())


class UpdateAccessRequestQueryParams(serializers.Serializer):
    """Request serializer for PUT /v1/users/access/subfunctions query params."""

    id = serializers.IntegerField(min_value=1)
