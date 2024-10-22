"""
`BI Portal` `Function` view module. Views handle requests to
create, fetch, update, and delete records within the `Function`
table. `Function` helps to classify a resource within a primary
organizational unit that encompasses a broad area of expertise
and responsibilities within the organization. `Function` shares
an indirect relationship with `Resource` through related
subfunctions.
"""

import logging
from typing import List, Union

from django import http
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from directory import exceptions, controllers
from directory.models.Function.serializers import FunctionSerializer
from directory.views import serializers


from manager.cache.decorators import cache_request, DEFAULT_TIMEOUT
from manager.utils.decorators import with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


class Function(View):
    """
    Handle user requests to create, fetch, update, and delete `Function`
    records for `BI Portal`. `Function` helps to classify a resource within
    a primary organizational unit that encompasses a broad area of expertise
    and responsibilities within the organization.
    """

    @method_decorator(with_serializer(serializers.FetchFunctionRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/directory/functions."""

        try:
            request_params = f"?id={body['id']}" if body["id"] else ""
            LOGGER.info(f"GET /v1/directory/functions{request_params}")

            # Fetch a `Function` record given its id,
            # else all `Function` records.
            functions = controllers.Function.fetch_functions(body["id"])

            # Set many field.
            many: bool = body["id"] is None

            # Serialize `Function`(s).
            data: Union[dict, List[dict]] = FunctionSerializer(
                functions, many=many
            ).data

            return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except exceptions.DirectoryError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
