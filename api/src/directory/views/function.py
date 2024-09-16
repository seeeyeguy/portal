"""
`BI Portal` `Function` view module. Views handle requests to
create, fetch, update, and delete records within the `Function`
table. `Function` helps to classify a resource within a primary
organizational unit that encompasses a broad area of expertise
and responsibility within the organization. `Function` shares
an indirect relationship with `Resource` through related
subfunctions.
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


class Function(View):
    """
    Handle user requests to create, fetch, update, and delete `Function`
    records for `BI Portal`. `Function` helps to classify a resource within
    a primary organizational unit that encompasses a broad area of expertise
    and responsibility within the organization.
    """

    @method_decorator(with_serializer(serializers.FetchFunctionRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: http.HttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/directory/functions."""

        request_params = f"?id={body['id']}" if body["id"] else ""
        LOGGER.info(f"GET /v1/directory/functions{request_params}")
        return http.JsonResponse([], status=status.HTTP_200_OK, safe=False)
