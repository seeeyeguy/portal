"""
Serializers for `Request` model. Serializers convert
python objects to JSON.
"""

from typing import cast, List, Union

from rest_framework import serializers

from request.models.Request.Request import Request
from request.models.Transition.Transition import Transition

from directory.models.Resource.serializers import ResourceSerializer
from request.models.Transition.serializers import TransitionSerializer
from users.models.Access.serializers import AccessSerializer


class RequestSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Request`."""

    resource = ResourceSerializer(read_only=True)
    originator = AccessSerializer(read_only=True)

    def to_representation(self, instance: Request) -> dict:
        record: dict = super().to_representation(instance)
        graph: dict[str, Union[dict[str, dict], None]] = {"latest": None, "nodes": {}}

        transitions = Transition.objects.filter(request__id=record["id"]).order_by(
            "-created"
        )
        transitions: List[dict] = TransitionSerializer(transitions, many=True).data

        for i, transition in enumerate(transitions):
            if i == 0:
                graph["latest"] = transition["id"]
            transition_id = cast(int, transition["id"])
            graph["nodes"][str(transition_id)] = transition  # type: ignore[index]

        record["transitions"] = graph
        return record

    class Meta:
        """Meta for `Request` serializer."""

        model = Request
        fields = "__all__"
