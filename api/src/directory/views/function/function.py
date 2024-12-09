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
from django.contrib.auth.decorators import login_required
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

    @method_decorator(login_required)
    @method_decorator(with_serializer(serializers.CreateFunctionRequest))
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/directory/functions."""

        LOGGER.info("POST /v1/directory/functions.")

        function = controllers.Function.create_function(
            name=body["name"], description=body["description"]
        )
        return http.JsonResponse(function, status=status.HTTP_201_CREATED, safe=False)

    @method_decorator(login_required)
    @method_decorator(with_serializer(serializers.UpdateFunctionRequest))
    def put(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for PUT /v1/directory/functions."""

        req = serializers.UpdateFunctionRequestQueryParams(data=request.GET)

        if not req.is_valid():
            return http.JsonResponse(
                req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
            )

        function_id: int = req.validated_data.get("id")

        LOGGER.info(f"PUT /v1/directory/functions?id={function_id}.")

        function = controllers.Function.update_function(
            function_id=function_id, name=body["name"], description=body["description"]
        )
        return http.JsonResponse(function, status=status.HTTP_201_CREATED, safe=False)

    @method_decorator(login_required)
    @method_decorator(with_serializer(serializers.DeleteFunctionRequest))
    def delete(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for DELETE /v1/directory/functions."""

        LOGGER.info(f"DELETE /v1/directory/functions?id={body['id']}.")

        rows_affected = controllers.Function.delete_function(function_id=body["id"])
        return http.JsonResponse(rows_affected, status=status.HTTP_200_OK, safe=False)

    @method_decorator(with_serializer(serializers.FetchFunctionRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/directory/functions."""

        try:
            request_params = f"?id={body['id']}" if body["id"] else ""
            LOGGER.info(f"GET /v1/directory/functions{request_params}.")

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
