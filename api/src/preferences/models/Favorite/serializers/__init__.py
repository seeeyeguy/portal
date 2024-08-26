"""
Serializers for `Favorite` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from preferences.models.Favorite.Favorite import Favorite

from directory.models.Resource.serializers import ResourceSerializer
from users.models.User.serializers import UserSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Favorite`."""

    user = UserSerializer(read_only=True)
    resource = ResourceSerializer(read_only=True)

    class Meta:
        """Meta for `Favorite` serializer."""

        model = Favorite
        fields = "__all__"
