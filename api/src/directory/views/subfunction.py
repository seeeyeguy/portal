"""
`BI Portal` `SubFunction` view module. Views handle requests to
create, fetch, update, and delete records within the `SubFunction`
table. `SubFunction` helps to classify a resource within a specialized
division within a `Function` that focuses on a more specific area
of expertise.
"""

import logging

from django import http
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from directory.views import serializers

from manager.cache.decorators import cache_request, DEFAULT_TIMEOUT
from manager.utils.decorators import with_serializer

LOGGER = logging.getLogger(__name__)


class SubFunction(View):
    """
    Handle user requests to create, fetch, update, and delete `SubFunction`
    records for `BI Portal`. `SubFunction` helps to classify a resource within
    a specialized division within a `Function` that focuses on a more specific
    area of expertise.
    """

    @method_decorator(with_serializer(serializers.FetchSubFunctionRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: http.HttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/directory/subfunctions."""

        request_params = f"?id={body['id']}" if body["id"] else ""
        LOGGER.info(f"GET /v1/directory/subfunctions{request_params}")
        return http.JsonResponse([], status=status.HTTP_200_OK, safe=False)
