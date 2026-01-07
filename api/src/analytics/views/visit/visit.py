"""
`BI Portal` `Visit` view module. Views handle requests to
create, fetch, update, and delete records within the `Visit`
table. `Visit` provides insights into users' behavior,
particularly in regards to the use of resources.
"""

# Remove pylint disable in implementation story.
# pylint: disable=unused-argument
import logging
from typing import Any
from django import http
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from analytics import controllers, exceptions
from analytics.models.Visit.serializers import VisitSerializer
from analytics.views import serializers

from manager.cache.decorators import cache_request, DEFAULT_TIMEOUT
from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest
from directory.models import Resource
from django.contrib.auth import get_user_model


LOGGER = logging.getLogger(__name__)


class Visit(View):
    """
    Handle user requests to create, fetch, update, and delete `Visit`
    records for `BI Portal`. `Visit` stores and tracks resource
    utilization data for users.
    """

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializer_class=serializers.CreateVisitRequest))
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/analytics/visits."""

        try:
            LOGGER.info("POST /v1/analytics/visits.")

            user_email: str = request.user.email

            # Create `Visit`.
            visit = controllers.Visit.create_visit(
                user=user_email, resource=body["resource"]
            )

            # Serialize Visit.
            data: dict = VisitSerializer(visit).data
            return http.JsonResponse(data, status=status.HTTP_201_CREATED)
        except exceptions.AnalyticsError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(with_serializer(serializer_class=serializers.FetchVisitRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(
        self,
        request: DjangoHttpRequest,
        params: dict,
        *args: Any,
        **kwargs: Any,
    ) -> http.JsonResponse:
        """Endpoint for GET /v1/analytics/visits."""

        # Disallow mixing top with page/limit
        if params.get("top") and (params.get("page") or params.get("limit")):
            return http.JsonResponse(
                {"detail": "Cannot use 'top' together with 'page' or 'limit'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Resource existence check
        if params.get("resource") is not None:
            resource_id = params["resource"]
            if not Resource.objects.filter(
                id=resource_id, active=True, deleted=False
            ).exists():
                return http.JsonResponse(
                    {"detail": "Resource not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        # User existence check
        if params.get("user"):
            User = get_user_model()
            if not User.objects.filter(username__iexact=params["user"]).exists():
                return http.JsonResponse(
                    {"detail": "User not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        # Log query string
        query_str = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
        LOGGER.info(f"GET /v1/analytics/visits?{query_str}")

        # Controller call
        visits = controllers.Visit.fetch_visited_resource(
            user=params.get("user"),
            resource=params.get("resource"),
            page=params.get("page"),
            limit=params.get("limit"),
            top=params.get("top"),
        )

        return http.JsonResponse(visits, status=status.HTTP_200_OK, safe=False)
