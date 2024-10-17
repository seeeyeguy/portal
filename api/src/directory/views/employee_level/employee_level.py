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

from manager.cache.decorators import cache_request, DEFAULT_TIMEOUT
from manager.utils.decorators import with_serializer

LOGGER = logging.getLogger(__name__)


class EmployeeLevel(View):
    """
    Handle user requests to create, fetch, update, and delete `EmployeeLevel`
    records for `BI Portal`. `EmployeeLevel` helps to classify a resource
    within an organization hierarchial level of concern.
    """

    @method_decorator(with_serializer(serializers.FetchEmployeeLevelRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: http.HttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/directory/employee-levels."""

        try:
            request_params: str = f"?id={body['id']}" if body["id"] else ""
            LOGGER.info(f"GET /v1/directory/employee-levels{request_params}")

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
