"""
`BI Portal` `QueryFilterState` view module. Views handle requests to
create, fetch, update, and delete records within the `QueryFilterState`
table. `QueryFilterState` represents a user's preferred state of filters
for the `BI Portal` application.
"""
# Remove pylint disable in implementation story.
# pylint: disable=unused-argument
import logging

from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from preferences import controllers, exceptions
from preferences.models.QueryFilterState.serializers import QueryFilterStateSerializer
from preferences.views import serializers

from manager.utils.decorators import with_serializer

LOGGER = logging.getLogger(__name__)


class QueryFilterState(LoginRequiredMixin, View):
    """
    Handle user requests to create, fetch, update, and delete `QueryFilterState`
    records for `BI Portal`. `QueryFilterState` represents a user's preferred state
    of filters for the `BI Portal` application.
    """

    @method_decorator(with_serializer(serializers.CreateQueryFilterStateRequest))
    def post(self, request: http.HttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/preferences/query-filter-state."""

        try:
            LOGGER.info("POST /v1/preferences/query-filter-state.")

            # Call controller to create `QueryFilterState`.
            query_filter_state = controllers.QueryFilterState.create_query_filter_state(
                user=body["user"],
                search=body["search"],
                functions=body["functions"],
                employee_levels=body["employee_levels"],
                tags=body["tags"],
            )

            # Serialize `QueryFilterState`.
            data: dict = QueryFilterStateSerializer(query_filter_state).data
            return http.JsonResponse(data, status=status.HTTP_201_CREATED)
        except exceptions.PreferencesError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(with_serializer(serializers.UpdateQueryFilterStateRequest))
    def put(self, request: http.HttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for PUT /v1/preferences/query-filter-state."""

        req = serializers.UpdateQueryFilterStateQueryParams(data=request.GET)
        if not req.is_valid():
            return http.JsonResponse(
                req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
            )

        record_id = req.validated_data.get("id")

        LOGGER.info(
            f"PUT /v1/preferences/query-filter-state?id={record_id}.",
        )

        query_filter_state = controllers.QueryFilterState.update_query_filter_state(
            record_id=record_id,
            search=body["search"],
            functions=body["functions"],
            employee_levels=body["employee_levels"],
            tags=body["tags"],
        )
        return http.JsonResponse(query_filter_state, status=status.HTTP_201_CREATED)

    @method_decorator(with_serializer(serializers.FetchQueryFilterStateRequest))
    def get(self, request: http.HttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/preferences/query-filter-state."""

        LOGGER.info(f"GET /v1/preferences/query-filter-state?user={body['user']}.")

        query_filter_state = controllers.QueryFilterState.fetch_query_filter_state(
            user=body["user"]
        )
        return http.JsonResponse(
            query_filter_state, status=status.HTTP_200_OK, safe=False
        )
