"""
Serializers for `Disposition` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from request.models.Disposition.Disposition import Disposition

from request.models.Transition.serializers import TransitionSerializer
from users.models.Access.serializers import AccessSerializer


class DispositionSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Disposition`."""

    approver = AccessSerializer(read_only=True)
    transition = TransitionSerializer(read_only=True)

    class Meta:
        """Meta for `Disposition` serializer."""

        model = Disposition
        fields = "__all__"
