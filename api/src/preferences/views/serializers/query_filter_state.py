"""
Serializers for requests to `QueryFilterState` views. Serializers provide
validation for request parameters.
"""

from rest_framework import serializers


class QueryFilterStateBaseRequest(serializers.Serializer):
    """Base serializer for `QueryFilterState` requests."""

    user = serializers.EmailField()


class QueryFilterStateBasePostRequest(serializers.Serializer):
    """
    Base serializer for `QueryFilterState` requests to
    modify/create a record.
    """

    search = serializers.IntegerField(allow_null=True)
    functions = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True
    )
    employee_levels = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=True
    )
    tags = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)


class CreateQueryFilterStateRequest(
    QueryFilterStateBaseRequest, QueryFilterStateBasePostRequest
):
    """Request serializer for POST /v1/preferences/query-filter-state."""


class UpdateQueryFilterStateRequest(QueryFilterStateBasePostRequest):
    """Request serializer for PUT /v1/preferences/query-filter-state."""


class UpdateQueryFilterStateQueryParams(serializers.Serializer):
    """Request serializer for PUT /v1/preferences/query-filter-state query params."""

    id = serializers.IntegerField()


class FetchQueryFilterStateRequest(QueryFilterStateBaseRequest):
    """Request serializer for GET /v1/preferences/query-filter-state."""
