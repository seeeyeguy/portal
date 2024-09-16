"""
`BI Portal` `Resource` view module. Views handle requests to
create, fetch, search, update, and delete records within the
`Resource` table. `Resource` represents a link to an internal
tool within L3Harris technologies. `Resource` is the primary
content served by `BI Portal`.
"""
# Remove pylint disable in implementation story.
# pylint: disable=unused-argument
import logging

from django import http
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from directory.views import serializers

from manager.cache.decorators import cache_request, DEFAULT_TIMEOUT
from manager.utils.decorators import with_serializer

LOGGER = logging.getLogger(__name__)


class ResourceSearch(View):
    """
    Handle user requests to search for `Resource` records in `BI Portal`.
    `Resource` represents a link to an internal tool within L3Harris
    technologies.
    """

    @method_decorator(
        with_serializer(serializer_class=serializers.ResourceSearchRequest)
    )
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def post(self, request: http.HttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/directory/resources/search."""

        req = serializers.ResourceSearchQueryParams(data=request.GET)
        if not req.is_valid():
            return http.JsonResponse(
                req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
            )

        page = req.validated_data.get("page")
        limit = req.validated_data.get("limit")

        request_params = f"?page={page}" if page else ""
        request_params = (
            f"{request_params}{'&' if page else '?'}limit={limit}"
            if limit
            else request_params
        )

        LOGGER.info(f"POST /v1/directory/resources/search{request_params}.")
        return http.JsonResponse([], status=status.HTTP_200_OK, safe=False)
