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
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from preferences import controllers, exceptions, models
from preferences.models.QueryFilterState.serializers import QueryFilterStateSerializer
from preferences.views import serializers
from preferences.utils.constants.response import CACHE_CONTROL_NO_CACHE

from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


class QueryFilterState(View):
    """
    Handle user requests to create, fetch, update, and delete `QueryFilterState`
    records for `BI Portal`. `QueryFilterState` represents a user's preferred state
    of filters for the `BI Portal` application.
    """

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.CreateQueryFilterStateRequest))
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/preferences/query-filter-state."""

        try:
            LOGGER.info("POST /v1/preferences/query-filter-state.")

            # Call controller to create `QueryFilterState`.
            query_filter_state = controllers.QueryFilterState.create_query_filter_state(
                user=request.user.username,
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

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.UpdateQueryFilterStateRequest))
    def put(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for PUT /v1/preferences/query-filter-state."""

        try:
            req = serializers.UpdateQueryFilterStateQueryParams(data=request.GET)

            if not req.is_valid():
                return http.JsonResponse(
                    req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
                )

            record_id = req.validated_data.get("id")

            LOGGER.info(
                f"PUT /v1/preferences/query-filter-state?id={record_id}.",
            )

            # Update the `QueryFilterState`.
            query_filter_state = controllers.QueryFilterState.update_query_filter_state(
                record_id=record_id,
                search=body["search"],
                functions=body["functions"],
                employee_levels=body["employee_levels"],
                tags=body["tags"],
                user=request.user.username,
            )

            # Serialize `QueryFilterState`.
            data: dict = QueryFilterStateSerializer(query_filter_state).data

            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
        except exceptions.PreferencesError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.FetchQueryFilterStateRequest))
    def get(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/preferences/query-filter-state."""

        try:

            request_params = f"?user={body['user']}"
            LOGGER.info(f"GET /v1/preferences/query-filter-state{request_params}")

            # Fetch a `QueryFilterState` record given a user's email.
            query_filter_state: models.QueryFilterState = (
                controllers.QueryFilterState.fetch_query_filter_state(user=body["user"])
            )

            # Serialize `QueryFilterState`.
            data: dict = QueryFilterStateSerializer(query_filter_state).data

            return http.JsonResponse(
                data,
                status=status.HTTP_200_OK,
                headers={**CACHE_CONTROL_NO_CACHE},
                safe=False,
            )
        except exceptions.PreferencesError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
