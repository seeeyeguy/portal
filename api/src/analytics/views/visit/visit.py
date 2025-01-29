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
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from analytics import controllers, exceptions
from analytics.models.Visit.serializers import VisitSerializer
from analytics.views import serializers

from manager.cache.decorators import cache_request, DEFAULT_TIMEOUT
from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

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

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializer_class=serializers.FetchVisitRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/analytics/visits."""

        request_params = f"?id={body['id']}" if body["id"] else ""
        request_params = (
            f"?user={body['user']}" if body["user"] != "" else request_params
        )
        request_params = (
            f"{request_params}{'&' if body['user'] else '?'}resource={body['resource']}"
            if body["resource"]
            else request_params
        )
        request_params = (
            # pylint: disable=line-too-long
            f"{request_params}{'&' if body['user'] or body['resource'] else '?'}page={body['page']}"
            if body["page"]
            else request_params
        )
        # pylint: disable=line-too-long
        request_params = (
            f"{request_params}{'&' if body['user'] or body['resource'] or body['page'] else '?'}limit={body['limit']}"
            if body["limit"]
            else request_params
        )

        LOGGER.info(f"GET /v1/analytics/visits{request_params}.")
        visits = controllers.Visit.fetch_visit(
            record_id=body["id"],
            user=body["user"],
            resource=body["resource"],
            page=body["page"],
            limit=body["limit"],
        )
        return http.JsonResponse(visits, status=status.HTTP_200_OK)
