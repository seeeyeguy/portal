"""
`BI Portal` `Disposition` view module. Views handle requests to
create records within the `Disposition` table through
the Request/Response cycle. `Disposition` represents
a vote by a BI Portal admin on a request to add/modify
a directory resource.
"""

import logging
from typing import List
from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer
from django import http
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from request import controllers, exceptions
from request.models.Disposition.serializers import DispositionSerializer
from request.views import serializers

from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


class Disposition(View):
    """
    Handle user requests to create and fetch `Disposition` records
    for `BI Portal`. `Disposition` represents a vote by a BI Portal
    admin on a request to add/modify a directory resource.
    """

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.CreateDispositionRequest))
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/request/disposition."""

        try:
            LOGGER.info("POST /v1/request/disposition.")

            # Call controller to create `Disposition`.
            disposition = controllers.Disposition.create_disposition(
                approver=request.user,
                request=body["request_id"],
                disposition=body["disposition"],
                justification=body.pop("justification", ""),
            )

            # Serialize `Disposition`.
            data: dict = DispositionSerializer(disposition).data

            # Broadcast to WebSocket group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "asgi_api_disposition",
                {
                    "type": "disposition.message",
                    "payload": {
                        "status": 201,
                        "resourceId": disposition.transition.request.resource.id,
                        "resourceName": disposition.transition.request.resource.name,
                        "disposition": disposition.disposition,
                        "firstName": disposition.approver.user.first_name,
                        "lastName": disposition.approver.user.last_name,
                        "content": "Disposition created successfully.",
                    },
                },
            )

            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
        except exceptions.RequestError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
