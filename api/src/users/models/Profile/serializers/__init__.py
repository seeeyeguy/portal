"""
Serializers for `Profile` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from users.models import Profile

from users.models.Segment.serializers import SegmentSerializer
from users.models.User.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Profile`."""

    user = UserSerializer(read_only=True)
    segment = SegmentSerializer(read_only=True)

    class Meta:
        """Meta for `Profile` serializer."""

        model = Profile
        fields = "__all__"
