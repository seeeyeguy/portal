"""
Serializers for requests to `Resource` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class BaseResourceRequest(serializers.Serializer):
    """Base serializer used for POST and PUT /v1/directory/resources requests."""

    name = serializers.CharField(max_length=512)
    description = serializers.CharField(min_length=30, max_length=8192)
    url = serializers.URLField()
    thumbnail = serializers.ImageField(allow_null=True)
    employee_levels = serializers.ListField(child=serializers.IntegerField())
    subfunctions = serializers.ListField(child=serializers.IntegerField())
    tags = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True, default=[]
    )
    point_of_contacts = serializers.ListField(child=serializers.EmailField())
    type = serializers.CharField(max_length=512)
    download = serializers.BooleanField()


class CreateResourceRequest(BaseResourceRequest):
    """Request serializer for POST /v1/directory/resources"""

    previous_revision = serializers.IntegerField(
        allow_null=True, default=None, min_value=1
    )
    uid = serializers.UUIDField(format="hex_verbose", allow_null=True, default=None)


class UpdateResourceRequest(BaseResourceRequest):
    """Request serializer for PUT /v1/directory/resources"""

    thumbnail = serializers.ImageField(allow_null=True, default=None)


class UpdateResourceRequestQueryParams(serializers.Serializer):
    """Request serializer for PUT /v1/directory/resources query params."""

    id = serializers.IntegerField()


class FetchResourceRequest(serializers.Serializer):
    """Request serializer for GET /v1/directory/resources."""

    id = serializers.IntegerField(allow_null=True, default=None)
    page = serializers.IntegerField(allow_null=True, default=None)
    limit = serializers.IntegerField(allow_null=True, default=None)


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
    download = serializers.BooleanField(allow_null=True, default=None)
    structure = serializers.ChoiceField(
        choices=["default", "functree"], default="default"
    )


class ResourceSearchQueryParams(serializers.Serializer):
    """Request serializer for POST /v1/directory/resources/search query params."""

    page = serializers.IntegerField(allow_null=True, default=None)
    limit = serializers.IntegerField(allow_null=True, default=None)
