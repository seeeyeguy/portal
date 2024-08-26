"""
Serializers for `Transition` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from request.models.Transition.Transition import Transition

from request.models.Request.serializers import RequestSerializer
from request.models.Stage.serializers import StageSerializer


class TransitionSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Transition`."""

    request = RequestSerializer(read_only=True)
    stage = StageSerializer(read_only=True)
    previous_transition = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """Meta for `Transition` serializer."""

        model = Transition
        fields = "__all__"
