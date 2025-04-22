"""
Serializers for `Transition` model. Serializers convert
python objects to JSON.
"""

from rest_framework import serializers

from request.models.Disposition.Disposition import Disposition
from request.models.Transition.Transition import Transition

from request.models.Stage.serializers import StageSerializer
from users.models.Access.serializers import AccessSerializer


class DispositionSerializerReverseRelation(serializers.ModelSerializer):
    """Model Serializer for `Transition` `Disposition`
    reverse relation."""

    approver = AccessSerializer(read_only=True)
    transition = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """Meta for `Disposition` serializer."""

        model = Disposition
        fields = "__all__"


class TransitionSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Transition`."""

    request = serializers.PrimaryKeyRelatedField(read_only=True)
    stage = StageSerializer(read_only=True)
    previous_transition = serializers.PrimaryKeyRelatedField(read_only=True)

    def to_representation(self, instance: Transition) -> dict:
        record: dict = super().to_representation(instance)

        dispositions = Disposition.objects.select_related("approver").filter(
            transition__id=record["id"]
        )
        record["dispositions"] = DispositionSerializerReverseRelation(
            dispositions, many=True
        ).data

        return record

    class Meta:
        """Meta for `Transition` serializer."""

        model = Transition
        fields = "__all__"
