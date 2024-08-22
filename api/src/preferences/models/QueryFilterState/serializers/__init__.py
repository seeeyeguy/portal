"""
Serializers for `QueryFilterState` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from preferences.models.QueryFilterState.QueryFilterState import QueryFilterState

from analytics.models.Query.serializers import QuerySerializer
from users.models.User.serializers import UserSerializer


class QueryFilterStateSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `QueryFilterState`."""

    search = QuerySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    functions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    employee_levels = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        """Meta for `QueryFilterState` serializer."""

        model = QueryFilterState
        fields = "__all__"
