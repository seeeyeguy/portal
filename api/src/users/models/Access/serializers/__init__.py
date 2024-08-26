"""
Serializers for `Access` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

# pylint: disable=ungrouped-imports
from users.models.Access.Access import Access

from request.models.Stage.serializers import StageSerializer
from users.models.Role.serializers import RoleSerializer
from users.models.User.serializers import UserSerializer


class AccessSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Access`."""

    user = UserSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    stage = StageSerializer(many=True, read_only=True)

    class Meta:
        """Meta for `Access` serializer."""

        model = Access
        fields = "__all__"
