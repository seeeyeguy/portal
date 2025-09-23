"""
`Program Review Tool` `ReportingPeriod` view module. Views handle requests to
fetch reporting periods from external source.
"""

import logging

from django import http
from django.utils.decorators import method_decorator
from django.views import View

from program_review_tool import controllers
from program_review_tool.views import serializers

from manager.cache.decorators import (
    cache_request,
    DEFAULT_TIMEOUT,
)
from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest


LOGGER = logging.getLogger(__name__)


class ReportingPeriod(View):
    """
    Handle user requests to fetch reporting periods
    from an external source for `Program Review Tool`.
    """

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.FetchReportingPeriodRequest))
    @method_decorator(cache_request(DEFAULT_TIMEOUT))
    def get(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /program-review-tool/reporting-period."""

        previous_period_count: int = body["previous_period_count"]

        request_params = (
            f"?previous_period_count={previous_period_count}"
            if previous_period_count
            else ""
        )

        LOGGER.info(f"GET /program-review-tool/reporting-period{request_params}")

        reporting_periods = controllers.ReportingPeriod.fetch_reporting_periods(
            previous_period_count=previous_period_count
        )

        return http.JsonResponse(reporting_periods, status=200, safe=False)
