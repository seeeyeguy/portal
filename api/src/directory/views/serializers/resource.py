"""
Serializers for requests to `Resource` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class ResourceSearchRequest(serializers.Serializer):
    """Request serializer for POST /v1/directory/resources/search."""

    name = serializers.CharField(max_length=512, allow_blank=True, default="")
    description = serializers.CharField(max_length=4096, allow_blank=True, default="")
    functions = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, default=[]
    )
    subfunctions = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, default=[]
    )
    employee_levels = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, default=[]
    )
    tags = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, default=[]
    )
    download = serializers.BooleanField(default=False)
    structure = serializers.ChoiceField(
        choices=["default", "functree"], default="default"
    )
    serialize = serializers.BooleanField(default=False)


class ResourceSearchQueryParams(serializers.Serializer):
    """Request serializer for POST /v1/directory/resources/search query params."""

    page = serializers.IntegerField(allow_null=True, default=None)
    limit = serializers.IntegerField(allow_null=True, default=None)
