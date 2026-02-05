"""
`BI Portal` `Content` view module. Views handle requests to
create, fetch, update, and delete records within the
`Content` table. `Content` represents dynamic content
within `BI Portal`.
"""

import logging

from django import http
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from content.controllers.Content.Content import Content as ContentController
from content.exceptions import ContentError
from content.models.Content.serializers import ContentSerializer
from content.utils.constants.response import CACHE_CONTROL_NO_CACHE
from content.views import serializers

from manager.cache.decorators import (
    invalidate_request_cache,
)
from manager.utils.decorators import admin_required, login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


class Content(View):
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
    @method_decorator(invalidate_request_cache())
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

    @method_decorator(with_serializer(serializer_class=serializers.FetchContentRequest))
    def get(self, _: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/content/content."""

        try:
            LOGGER.info("GET /v1/content/content.")
            content = ContentController.fetch_content(key=body["key"])

            data: dict = ContentSerializer(content).data

            return http.JsonResponse(
                data=data,
                status=status.HTTP_200_OK,
                headers={**CACHE_CONTROL_NO_CACHE},
                safe=False,
            )
        except ContentError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(
                exc.message,
                status=exc.status,
                headers={**CACHE_CONTROL_NO_CACHE},
                safe=False,
            )

    @method_decorator(login_required())
    @method_decorator(admin_required())
    @method_decorator(
        with_serializer(serializer_class=serializers.UpdateContentRequest)
    )
    @method_decorator(invalidate_request_cache())
    def put(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for PUT /v1/content/content."""

        try:
            LOGGER.info("PUT /v1/content/content.")

            req = serializers.UpdateContentRequestQueryParams(data=request.GET)

            if not req.is_valid():
                return http.JsonResponse(
                    req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
                )

            content_key = req.validated_data.get("key")

            content = ContentController.update_content(
                key=content_key, content=body["content"], modified_by=request.user
            )

            data: dict = ContentSerializer(content).data

            return http.JsonResponse(
                data=data, status=status.HTTP_201_CREATED, safe=False
            )
        except ContentError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    @method_decorator(admin_required())
    @method_decorator(
        with_serializer(serializer_class=serializers.DeleteContentRequest)
    )
    @method_decorator(invalidate_request_cache())
    def delete(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for DELETE /v1/content/content."""

        LOGGER.info("DELETE /v1/content/content.")

        rows_affected = ContentController.delete_content(
            key=body["key"], deleted_by=request.user
        )

        data: int = rows_affected
        return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
