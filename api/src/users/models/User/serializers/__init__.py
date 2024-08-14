"""
Serializers for `User` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from django.contrib.auth import models as DjangoAuthModels


class UserSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `User`."""

    class Meta:
        """Meta for `User` serializer."""

    model = DjangoAuthModels.User
    fields = ["id", "username", "email", "first_name", "last_name", "is_active"]
