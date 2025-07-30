"""
`BI Portal` `EmployeeLevel` view module. Views handle requests to
create, fetch, update, and delete records within the `EmployeeLevel`
table. `EmployeeLevel` helps to classify a resource within a field
of concern in regards to a hierarchial level within the organization
such as employee, manager, or executive.
"""

import logging
from typing import List, Union

from django import http
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from directory import controllers, exceptions
from directory.models.EmployeeLevel.serializers import EmployeeLevelSerializer
from directory.views import serializers

from manager.cache.decorators import (
    cache_request,
    DEFAULT_TIMEOUT,
    invalidate_request_cache,
)
from manager.utils.decorators import admin_required, login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


class EmployeeLevel(View):
    """
    Handle user requests to create, fetch, update, and delete `EmployeeLevel`
    records for `BI Portal`. `EmployeeLevel` helps to classify a resource
    within an organization hierarchial level of concern.
    """

    @method_decorator(login_required())
    @method_decorator(admin_required())
    @method_decorator(with_serializer(serializers.CreateEmployeeLevelRequest))
    @method_decorator(invalidate_request_cache())
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/directory/employee-levels."""

        try:
            LOGGER.info("POST /v1/directory/employee-levels.")

            employee_level = controllers.EmployeeLevel.create_employee_level(
                name=body["name"], description=body["description"], level=body["level"]
            )

            # Serialize `EmployeeLevel`.
            data: dict = EmployeeLevelSerializer(employee_level).data

            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
        except exceptions.DirectoryError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    @method_decorator(admin_required())
    @method_decorator(with_serializer(serializers.UpdateEmployeeLevelRequest))
    @method_decorator(invalidate_request_cache())
    def put(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for PUT /v1/directory/employee-levels."""

        try:

            req = serializers.UpdateEmployeeLevelRequestQueryParams(data=request.GET)

            if not req.is_valid():
                return http.JsonResponse(
                    req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
                )

            employee_level_id: int = req.validated_data.get("id")

            LOGGER.info(f"PUT /v1/directory/employee-levels?id={employee_level_id}.")

            employee_level = controllers.EmployeeLevel.update_employee_level(
                employee_level_id=employee_level_id,
                name=body["name"],
                description=body["description"],
            )

            # Serialize `EmployeeLevel`.
            data: dict = EmployeeLevelSerializer(employee_level).data

            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
        except exceptions.DirectoryError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    @method_decorator(admin_required())
    @method_decorator(with_serializer(serializers.DeleteEmployeeLevelRequest))
    @method_decorator(invalidate_request_cache())
    def delete(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for DELETE /v1/directory/employee-levels."""

        LOGGER.info(f"DELETE /v1/directory/employee-levels?id={body['id']}.")

        rows_affected = controllers.EmployeeLevel.delete_employee_level(
            employee_level_id=body["id"]
        )

        return http.JsonResponse(rows_affected, status=status.HTTP_200_OK, safe=False)

    @method_decorator(with_serializer(serializers.FetchEmployeeLevelRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/directory/employee-levels."""

        try:
            request_params: str = f"?id={body['id']}" if body["id"] else ""
            LOGGER.info(f"GET /v1/directory/employee-levels{request_params}.")

            # Fetch the `EmployeeLevel`(s).
            employee_levels = controllers.EmployeeLevel.fetch_employee_levels(
                body["id"]
            )

            # Determine the value for `many` parameter on the serializer.
            many: bool = body["id"] is None

            # Serialize `EmployeeLevel`(s).
            data: Union[dict | List[dict]] = EmployeeLevelSerializer(
                employee_levels, many=many
            ).data
            return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except exceptions.DirectoryError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
