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

from analytics import controllers
from analytics.views import serializers

from manager.cache.decorators import cache_request, DEFAULT_TIMEOUT
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
        query = controllers.Query.create_query(
            user=body["user"], search_term=body["search_term"]
        )
        return http.JsonResponse(query, status=status.HTTP_201_CREATED)

    @method_decorator(with_serializer(serializer_class=serializers.FetchQueryRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: http.HttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/analytics/queries."""

        request_params = f"?id={body['id']}" if body["id"] else ""
        request_params = (
            f"?user={body['user']}" if body["user"] != "" else request_params
        )
        request_params = (
            f"{request_params}{'&' if body['user'] else '?'}page={body['page']}"
            if body["page"]
            else request_params
        )
        request_params = (
            f"{request_params}{'&' if body['user'] or body['page'] else '?'}limit={body['limit']}"
            if body["limit"]
            else request_params
        )

        LOGGER.info(f"GET /v1/analytics/queries{request_params}.")
        queries = controllers.Query.fetch_query(
            record_id=body["id"],
            user=body["user"],
            page=body["page"],
            limit=body["limit"],
        )
        return http.JsonResponse(queries, status=status.HTTP_200_OK)
