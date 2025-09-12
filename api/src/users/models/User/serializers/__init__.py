"""
Serializers for `User` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from django.contrib.auth import models as DjangoAuthModels


class UserSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `User`."""

    def to_representation(self, instance: DjangoAuthModels.User) -> dict:
        record: dict = super().to_representation(instance)
        email_username, _ = record["email"].split("@")
        user_l3harris_email: str = f"{email_username}@l3harris.com"
        record["email"] = user_l3harris_email
        return record

    class Meta:
        """Meta for `User` serializer."""

        model = DjangoAuthModels.User
        fields = ["id", "username", "email", "first_name", "last_name", "is_active"]
