"""
`BI Portal` `EmployeeLevel` view module. Views handle requests to
create, fetch, update, and delete records within the `EmployeeLevel`
table. `EmployeeLevel` helps to classify a resource within a field
of concern in regards to a hierarchial level within the organization
such as employee, manager, or executive.
"""

import logging

from django import http
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from directory import controllers
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

        request_params = f"?id={body['id']}" if body["id"] else ""
        LOGGER.info(f"GET /v1/directory/employee-levels{request_params}")

        employee_levels = controllers.EmployeeLevel.fetch_employee_levels(body["id"])
        return http.JsonResponse(employee_levels, status=status.HTTP_200_OK, safe=False)
