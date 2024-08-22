"""
Serializers for `Role` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from users.models.Role.Role import Role


class RoleSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Role`."""

    class Meta:
        """Meta for `Role` serializer."""

        model = Role
        fields = "__all__"
