"""
`BI Portal` `SubFunction` view module. Views handle requests to
create, fetch, update, and delete records within the `SubFunction`
table. `SubFunction` helps to classify a resource within a specialized
division within a `Function` that focuses on a more specific area
of expertise.
"""

import logging
from typing import List, Union

from django import http
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from directory import controllers, exceptions
from directory.models.SubFunction.serializers import SubFunctionSerializer
from directory.views import serializers

from manager.cache.decorators import cache_request, DEFAULT_TIMEOUT
from manager.utils.decorators import with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


class SubFunction(View):
    """
    Handle user requests to create, fetch, update, and delete `SubFunction`
    records for `BI Portal`. `SubFunction` helps to classify a resource within
    a specialized division within a `Function` that focuses on a more specific
    area of expertise.
    """

    @method_decorator(login_required)
    @method_decorator(with_serializer(serializers.CreateSubFunctionRequest))
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/directory/subfunctions."""

        LOGGER.info("POST /v1/directory/subfunctions.")

        subfunction = controllers.SubFunction.create_subfunction(
            name=body["name"],
            description=body["description"],
            function=body["function"],
        )
        return http.JsonResponse(
            subfunction, status=status.HTTP_201_CREATED, safe=False
        )

    @method_decorator(login_required)
    @method_decorator(with_serializer(serializers.UpdateSubFunctionRequest))
    def put(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for PUT /v1/directory/subfunctions."""

        req = serializers.UpdateSubFunctionRequestQueryParams(data=request.GET)

        if not req.is_valid():
            return http.JsonResponse(
                req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
            )

        subfunction_id: int = req.validated_data.get("id")

        LOGGER.info(f"PUT /v1/directory/subfunctions?id={subfunction_id}.")

        subfunction = controllers.SubFunction.update_subfunction(
            subfunction_id=subfunction_id,
            name=body["name"],
            description=body["description"],
            function=body["function"],
        )
        return http.JsonResponse(
            subfunction, status=status.HTTP_201_CREATED, safe=False
        )

    @method_decorator(login_required)
    @method_decorator(with_serializer(serializers.DeleteSubFunctionRequest))
    def delete(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for DELETE /v1/directory/subfunctions."""

        LOGGER.info(f"DELETE /v1/directory/subfunctions?id={body['id']}.")

        rows_affected = controllers.SubFunction.delete_subfunction(
            subfunction_id=body["id"]
        )

        return http.JsonResponse(rows_affected, status=status.HTTP_200_OK, safe=False)

    @method_decorator(with_serializer(serializers.FetchSubFunctionRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/directory/subfunctions."""

        try:
            request_params = f"?id={body['id']}" if body["id"] else ""
            LOGGER.info(f"GET /v1/directory/subfunctions{request_params}.")

            # Fetch the `SubFunction`(s).
            subfunctions = controllers.SubFunction.fetch_subfunctions(body["id"])

            # Determine the value for `many` parameter on the serializer.
            many: bool = body["id"] is None

            # Serialize `SubFunction`(s).
            data: Union[dict | List[dict]] = SubFunctionSerializer(
                subfunctions, many=many
            ).data
            return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except exceptions.DirectoryError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
