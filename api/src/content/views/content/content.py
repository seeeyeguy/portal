"""
`BI Portal` `Content` view module. Views handle requests to
create, fetch, update, and delete records within the
`Content` table. `Content` represents dynamic content
within `BI Portal`.
"""

import logging

from django import http
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView

from content.controllers.Content.Content import Content as ContentController
from content.exceptions import ContentError
from content.models.Content.serializers import ContentSerializer
from content.views import serializers

from manager.utils.decorators import admin_required, login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


class Content(APIView):
    """
    Handle user requests to create, fetch, update, and delete `Content`
    records for `BI Portal`. `Content` represents dynamic content
    within `BI Portal`.
    """

    @method_decorator(login_required())
    @method_decorator(admin_required())
    @method_decorator(
        with_serializer(serializer_class=serializers.CreateContentRequest)
    )
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/content/content."""

        try:
            LOGGER.info("POST /v1/content/content.")

            content = ContentController.create_content(
                key=body["key"], content=body["content"], created_by=request.user
            )

            data: dict = ContentSerializer(content).data

            return http.JsonResponse(
                data=data, status=status.HTTP_201_CREATED, safe=False
            )
        except ContentError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
