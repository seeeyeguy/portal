"""
`BI Portal` `Visit` view module. Views handle requests to
create, fetch, update, and delete records within the `Visit`
table. `Visit` provides insights into users' behavior,
particularly in regards to the use of resources.
"""
# Remove pylint disable in implementation story.
# pylint: disable=unused-argument
import logging

from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from analytics.views import serializers

from manager.utils.decorators import with_serializer

LOGGER = logging.getLogger(__name__)


class Visit(LoginRequiredMixin, View):
    """
    Handle user requests to create, fetch, update, and delete `Visit`
    records for `BI Portal`. `Visit` stores and tracks resource
    utilization data for users.
    """

    @method_decorator(with_serializer(serializer_class=serializers.CreateVisitRequest))
    def post(self, request: http.HttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/analytics/visits."""

        LOGGER.info("POST /v1/analytics/visits.")
        return http.JsonResponse({}, status=status.HTTP_201_CREATED)
