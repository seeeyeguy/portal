"""
`Program Review Tool` `Record` view module. Views handle requests to
create and fetch records within the `Record` table.
"""

import logging

from django import http
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views import View
from rest_framework import status

from program_review_tool import controllers, exceptions
from program_review_tool.models.Record.serializers import RecordSerializer
from program_review_tool.views import serializers

from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


@method_decorator(never_cache, name="dispatch")
class Record(View):
    """
    Handle user requests to create and fetch
    `Record`s for `Program Review Tool`.
    """

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.CreateRecordRequest))
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /program-review-tool/record."""

        LOGGER.info("POST /program-review-tool/record.")

        try:
            # Create `Record`.
            record = controllers.Record.create_record(
                user=request.user,
                pa_number=body["pa_number"],
                reporting_period=body["reporting_period"],
                name=body["name"],
                segment=body["segment"],
                sector=body["sector"],
                division=body["division"],
                tier=body["tier"],
                program_phase=body["program_phase"],
                site=body["site"],
                defense_financial_acquisition_regulation_clause=body[
                    "defense_financial_acquisition_regulation_clause"
                ],
                cost_and_software_data_reporting_system_clause=body[
                    "cost_and_software_data_reporting_system_clause"
                ],
                earned_value_management_system_reporting_requirement=body[
                    "earned_value_management_system_reporting_requirement"
                ],
                contract_type=body["contract_type"],
                contract_number=body["contract_number"],
                contract_value=body["contract_value"],
                contract_start_date=body["contract_start_date"],
                contract_end_date=body["contract_end_date"],
                actual_cost_work_performed_cumulative=body[
                    "actual_cost_work_performed_cumulative"
                ],
                budgeted_cost_work_performed_cumulative=body[
                    "budgeted_cost_work_performed_cumulative"
                ],
                budgeted_cost_work_scheduled_cumulative=body[
                    "budgeted_cost_work_scheduled_cumulative"
                ],
                cost_performance_index_cumulative=body[
                    "cost_performance_index_cumulative"
                ],
                schedule_performance_index_cumulative=body[
                    "schedule_performance_index_cumulative"
                ],
                budget_at_complete=body["budget_at_complete"],
                estimate_at_complete=body["estimate_at_complete"],
                estimate_to_complete=body["estimate_to_complete"],
                management_reserve=body["management_reserve"],
                weighted_risks_and_opportunities=body[
                    "weighted_risks_and_opportunities"
                ],
                customer_assessment=body["customer_assessment"],
                technical_assessment=body["technical_assessment"],
                risk_assessment=body["risk_assessment"],
                overall_program=body["overall_program"],
                comments=body["comments"],
            )
            # Serialize `Record`.
            data: dict = RecordSerializer(record).data

            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
        except exceptions.ProgramReviewToolError as exc:
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    def get(self, request: DjangoHttpRequest) -> http.JsonResponse:
        """Endpoint for GET /program-review-tool/record."""

        try:
            req = serializers.FetchRecordRequestQueryParams(data=request.GET)

            if not req.is_valid():
                return http.JsonResponse(
                    req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
                )

            pa_number: str = req.validated_data.get("pa_number")
            reporting_period: int = req.validated_data.get("reporting_period")
            refresh: bool = req.validated_data.get("refresh")

            request_params = f"?pa_number={pa_number}&reporting_period={reporting_period}&refresh={refresh}"

            LOGGER.info(f"GET /program-review-tool/record{request_params}")

            # Fetch `Program`'s `Record` data for reporting period.
            record_data: dict = controllers.Record.fetch_record(
                pa_number=pa_number, reporting_period=reporting_period, refresh=refresh
            )

            return http.JsonResponse(record_data, status=200, safe=False)
        except exceptions.ProgramReviewToolError as exc:
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
