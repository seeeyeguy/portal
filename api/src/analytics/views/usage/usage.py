"""
`BI Portal` `Usage` view module.

Handles GET requests to fetch usage records from the `Usage` table.
Delegates filtering, validation, and pagination logic to the controller.
Each response entry includes metadata such as the usage ID, username,
associated programs, creation timestamp, duration, success flag,
and any error message.
"""

# Standard library imports
import logging

# Third‑party library imports
from django import http
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

# Local application imports
from analytics import exceptions
from analytics.views import serializers
from manager.cache.decorators import cache_request, DEFAULT_TIMEOUT
from manager.utils.decorators import with_serializer
from manager.utils.types.request import DjangoHttpRequest
from program_review_tool import controllers

LOGGER = logging.getLogger(__name__)


class UsageView(View):
    """
    Handle user requests to fetch `Usage` records for `BI Portal`.

    The `Usage` model tracks program execution and resource utilization
    data for users. This view delegates filtering, validation, and
    pagination logic to the controller, and returns JSON responses
    containing metadata such as ID, associated user, programs,
    creation timestamp, duration, success flag, and error messages.
    """

    @method_decorator(with_serializer(serializer_class=serializers.FetchUsageRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/analytics/prt/usage."""

        try:
            # Build request params string for logging (same style as QueryView)
            request_params = f"?id={body['id']}" if body.get("id") else ""
            request_params = (
                f"{request_params}&user={body['user']}"
                if body.get("user")
                else request_params
            )
            request_params = (
                f"{request_params}{'&' if (body.get('id') or body.get('user')) else '?'}page={body['page']}"
                if body.get("page")
                else request_params
            )
            request_params = (
                f"{request_params}{'&' if (body.get('id') or body.get('user') or body.get('page')) else '?'}limit={body['limit']}"
                if body.get("limit")
                else request_params
            )
            request_params = (
                f"{request_params}&pa_number={body['pa_number']}"
                if body.get("pa_number")
                else request_params
            )
            request_params = (
                f"{request_params}&success={body['success']}"
                if body.get("success") is not None
                else request_params
            )

            LOGGER.info(f"GET /v1/analytics/prt/usage{request_params}.")

            # Call controller — all filtering/pagination handled there
            usages = controllers.Usage.fetch_usage(
                user=body.get("user"),
                page=body.get("page"),
                limit=body.get("limit"),
                pa_number=body.get("pa_number"),
                success=body.get("success"),
            )

            is_many = body.get("id") is None
            data = [
                {
                    "id": usage.pk,
                    "user": usage.user.username,
                    "programs": usage.programs,
                    "created": usage.created,
                    "duration": usage.duration,
                    "success": usage.success,
                    "error_msg": usage.error_msg,
                }
                for usage in usages
            ]

            return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)

        except exceptions.AnalyticsError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
