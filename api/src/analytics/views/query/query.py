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
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from analytics import controllers, exceptions
from analytics.models.Query.serializers import QuerySerializer
from analytics.views import serializers

from manager.cache.decorators import cache_request, DEFAULT_TIMEOUT
from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


class Query(View):
    """
    Handle user requests to create, fetch, update, and delete `Query`
    records for `BI Portal`. `Query` stores and tracks search data
    for users.
    """

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializer_class=serializers.CreateQueryRequest))
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/analytics/queries."""

        try:
            LOGGER.info("POST /v1/analytics/queries.")
            query = controllers.Query.create_query(
                user=request.user.username, search_term=body["search_term"]
            )
            # Serialize `Query`.
            data: dict = QuerySerializer(query).data
            return http.JsonResponse(data, status=status.HTTP_201_CREATED)
        except exceptions.AnalyticsError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(with_serializer(serializer_class=serializers.FetchQueryRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/analytics/queries."""

        try:
            request_params = f"?id={body['id']}" if body["id"] else ""
            request_params = (
                f"?resource={body['resource_id']}"
                if body["resource_id"]
                else request_params
            )
            request_params_with_resource_id = (
                f"{request_params}&user={body['user']}"
                if body["resource_id"]
                else f"?user={body['user']}"
            )
            request_params = (
                f"{request_params_with_resource_id}"
                if body["user"] != ""
                else request_params
            )
            request_params = (
                f"{request_params}{'&' if (body['resource_id'] or body['user']) else '?'}page={body['page']}"
                if body["page"]
                else request_params
            )
            request_params = (
                # pylint: disable=line-too-long
                f"{request_params}{'&' if (body['resource_id'] or body['user'] or body['page']) else '?'}limit={body['limit']}"
                if body["limit"]
                else request_params
            )
            request_params = (
                f"{request_params}&search_term={body['search_term']}"
                if body.get("search_term")
                else request_params
            )

            LOGGER.info(f"GET /v1/analytics/queries{request_params}.")

            queries = controllers.Query.fetch_query(
                record_id=body["id"],
                resource_id=body["resource_id"],
                user=body["user"],
                page=body["page"],
                limit=body["limit"],
                search_term=body.get("search_term"),
            )

            is_many = body["id"] is None

            data: dict = QuerySerializer(queries, many=is_many).data

            return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except exceptions.AnalyticsError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
