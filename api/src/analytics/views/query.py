"""
`BI Portal` `Query` view module. Views handle requests to
create, fetch, update, and delete records within the `Query`
table. `Query` provides insights into users' behavior,
particularly in regards to committed searches.
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


class Query(LoginRequiredMixin, View):
    """
    Handle user requests to create, fetch, update, and delete `Query`
    records for `BI Portal`. `Query` stores and tracks search data
    for users.
    """

    @method_decorator(with_serializer(serializer_class=serializers.CreateQueryRequest))
    def post(self, request: http.HttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/analytics/queries."""

        LOGGER.info("POST /v1/analytics/queries.")
        return http.JsonResponse({}, status=status.HTTP_201_CREATED)
