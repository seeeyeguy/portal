"""
`BI Portal` `Record` controller module. Controllers utilize the
Django ORM to create and fetch records within the `Record` table.
`Record` represents a Program's health and financials in a monthly snapshot,
captured through the `Program Performance Review (PPR)` Tool.
"""

import logging
import datetime
from typing import Union

from django.contrib.auth import models as AuthModels
from django.db.models import QuerySet

from program_review_tool import exceptions, models
from program_review_tool.models.Program.serializers import ProgramSerializer
from program_review_tool.models.Record.serializers import RecordSerializer

LOGGER = logging.getLogger(__name__)

# Default key-value pairs for program
# metrics data.
DEFAULT_PROGRAM_METRICS_DATA: dict = {
    "pa_number": "",
    "segment": "",
    "sector": "",
    "division": "",
    "tier": None,
    "contract_number": None,
    "contract_value": None,
    "contract_start_date": None,
    "contract_end_date": None,
    "actual_cost_work_performed_cumulative": None,
    "budgeted_cost_work_performed_cumulative": None,
    "budgeted_cost_work_scheduled_cumulative": None,
    "cost_performance_index_cumulative": None,
    "schedule_performance_index_cumulative": None,
    "budget_at_complete": None,
    "estimate_at_complete": None,
    "estimate_to_complete": None,
    "management_reserve": None,
    "weighted_risks_and_opportunities": None,
    "team_members": [],
}


# Default key-value pairs for shared `Record`
# metrics data.
DEFAULT_SHARED_RECORD_METRICS_DATA: dict = {
    "contract_type": "",
    "site": "",
    "cost_and_software_data_reporting_system_clause": None,
    "defense_financial_acquisition_regulation_clause": None,
    "earned_value_management_system_reporting_requirement": "",
    "program_phase": "",
}

# Default key-value pairs for current period's
# `Record` metrics data.
DEFAULT_CURRENT_PERIOD_RECORD_METRICS_DATA: dict = {
    "previous_revision": None,
    "customer_assessment": None,
    "technical_assessment": None,
    "risk_assessment": None,
    "overall_program": None,
    "comments": "",
    "user": None,
    "created": None,
}


class Record:
    """
    Container class for functions related to creating and
    retrieving `Record` records. `Record` represents a monthly snapshot
    of a `Program` within L3Harris Technologies, captured through the
    `Program Performance Review (PPR)` Tool.
    """

    @staticmethod
    def create_record(
        user: AuthModels.User,
        pa_number: str,
        reporting_period: int,
        name: str = "",
        segment: str = "",
        sector: str = "",
        division: str = "",
        tier: Union[int, None] = None,
        program_phase: str = "",
        site: str = "",
        defense_financial_acquisition_regulation_clause: Union[bool, None] = None,
        cost_and_software_data_reporting_system_clause: Union[bool, None] = None,
        earned_value_management_system_reporting_requirement: str = "",
        contract_type: str = "",
        contract_number: str = "",
        contract_value: Union[int, None] = None,
        contract_start_date: Union[datetime.date, None] = None,
        contract_end_date: Union[datetime.date, None] = None,
        actual_cost_work_performed_cumulative: Union[float, None] = None,
        budgeted_cost_work_performed_cumulative: Union[float, None] = None,
        budgeted_cost_work_scheduled_cumulative: Union[float, None] = None,
        cost_performance_index_cumulative: Union[float, None] = None,
        schedule_performance_index_cumulative: Union[float, None] = None,
        budget_at_complete: Union[float, None] = None,
        estimate_at_complete: Union[float, None] = None,
        estimate_to_complete: Union[float, None] = None,
        management_reserve: Union[float, None] = None,
        weighted_risks_and_opportunities: Union[float, None] = None,
        customer_assessment: Union[int, None] = None,
        technical_assessment: Union[int, None] = None,
        risk_assessment: Union[int, None] = None,
        overall_program: Union[int, None] = None,
        comments: str = "",
    ) -> models.Record:
        """
        Create a `Record` record in the database.

        Accepts:
            * user (AuthModels.User): The `User` that is creating the `Record`.
            * pa_number (str): PA number of related `Program` for the generated `Record`.
            * reporting_period (int): The reporting period.
            * name (str): The name of the `Program`.
            * segment (str): An organizational unit of L3Harris Technologies.
            * sector (str): An organizational unit of a segment.
            * division (str): An organizational unit of a sector.
            * tier (int | None): Describes the mission importance
                and risk of a `Program`. Limited to the range of 1-4, where 1 is
                considered the highest tier.
            * program_phase (str): The current phase of the `Program`.
            * site (str): The L3Harris Technologies site associated with the `Program`.
            * defense_financial_acquisition_regulation_clause (bool | None): Indicates whether the DFARS clause is applicable.
            * cost_and_software_data_reporting_system_clause (bool | None): Indicates whether the CSDR clause is applicable.
            * earned_value_management_system_reporting_requirement (str): The EVMS reporting requirement.
            * contract_type (str): The classification of the
                contract (e.g., FFP, CPFF, T&M) that defines terms of pricing,
                risk, and reimbursement.
            * contract_number (str): The unique identifier assigned
                to a contractual agreement between the customer and L3Harris technologies.
            * contract_value (int | None): The dollar value assigned to the `Program`.
            * contract_start_date (datetime.date | None): The date on which the contractual
                period of performance officially begins.
            * contract_end_date (datetime.date | None): The date on which the contractual period of
                performance is scheduled to conclude.
            * actual_cost_work_performed_cumulative (float | None): The total actual cost
                incurred for all completed work up to the reporting period.
            * budgeted_cost_work_performed_cumulative (float | None): The cumulative value
                of the budgeted cost for completed work as of the reporting period.
            * budgeted_cost_work_scheduled_cumulative (float | None): The cumulative value
                of the budgeted cost for work that was scheduled to be completed by the
                reporting period.
            * cost_performance_index_cumulative (float | None): A ratio (BCWP ÷ ACWP) that
                measures cost efficiency in executing the `Program`.
            * schedule_performance_index_cumulative (float | None): A ratio (BCWP ÷ BCWS)
                that measures schedule efficiency in completing the planned work.
            * budget_at_complete (float | None): The total budgeted cost for the
                entire scope of work as defined in the baseline plan.
            * estimate_at_complete (float | None): The current forecast of the total
                expected cost required to complete the `Program`.
            * estimate_to_complete (float | None): The projected additional cost needed
                to complete the remaining `Program` work (EAC - ACWP).
            * management_reserve (float | None): A budget set aside by management to cover
                unforeseen risks or changes outside the scope of baseline work.
            * weighted_risks_and_opportunities (float | None): The net financial impact of
                risks and opportunities, weighted by their probability of occurrence.
            * customer_assessment (int | none): The program manager's subjective customer assessment(1-4).
            * technical_assessment (int | none): The program manager's subjective technical assessment (1-4).
            * risk_assessment (int | none): The program manager's subjective risk assessment (1-4).
            * overall_program (int | none): The program manager's subjective overall program assessment (1-4).
            * comments (str): Additional comments.

        Returns:
            * record (models.Record): The newly created `Record` record.
        """

        try:

            if not (user and user.is_authenticated):
                raise exceptions.ProgramReviewToolError(
                    "Authentication required.", status=401
                )

            LOGGER.info(
                f"Creating Record for User: {user.email} for program: {pa_number} and reporting period: {reporting_period}."
            )

            # Fetch the associated `Program` instance.
            program_record = models.Program.objects.get(pa_number=pa_number)

            if not user.is_superuser:
                is_active_team_member = models.ProgramMember.objects.filter(
                    program_id=program_record.id,
                    user=user,
                    expiry_date__isnull=True,
                ).exists()
                if not is_active_team_member:
                    err_msg = "Permissions Denied."
                    LOGGER.error(err_msg)
                    raise exceptions.ProgramReviewToolError(err_msg, 403)

            previous_revision: Union[models.Record, None] = (
                models.Record.objects.filter(pa_number=pa_number).order_by("id").last()
            )

            record_data = {
                "user": user,
                "program": program_record,
                "pa_number": pa_number,
                "reporting_period": reporting_period,
                "previous_revision": previous_revision,
                "name": name,
                "segment": segment,
                "sector": sector,
                "division": division,
                "tier": tier,
                "program_phase": program_phase,
                "site": site,
                "defense_financial_acquisition_regulation_clause": defense_financial_acquisition_regulation_clause,
                "cost_and_software_data_reporting_system_clause": cost_and_software_data_reporting_system_clause,
                "earned_value_management_system_reporting_requirement": earned_value_management_system_reporting_requirement,
                "contract_type": contract_type,
                "contract_number": contract_number,
                "contract_value": contract_value,
                "contract_start_date": contract_start_date,
                "contract_end_date": contract_end_date,
                "actual_cost_work_performed_cumulative": actual_cost_work_performed_cumulative,
                "budgeted_cost_work_performed_cumulative": budgeted_cost_work_performed_cumulative,
                "budgeted_cost_work_scheduled_cumulative": budgeted_cost_work_scheduled_cumulative,
                "cost_performance_index_cumulative": cost_performance_index_cumulative,
                "schedule_performance_index_cumulative": schedule_performance_index_cumulative,
                "budget_at_complete": budget_at_complete,
                "estimate_at_complete": estimate_at_complete,
                "estimate_to_complete": estimate_to_complete,
                "management_reserve": management_reserve,
                "weighted_risks_and_opportunities": weighted_risks_and_opportunities,
                "customer_assessment": customer_assessment,
                "technical_assessment": technical_assessment,
                "risk_assessment": risk_assessment,
                "overall_program": overall_program,
                "comments": comments,
            }

            # Create the `Record` record.
            record: models.Record = models.Record.objects.create(**record_data)

            # Attach many‑to‑many `team_members` if exists.
            team_members = models.ProgramMember.objects.filter(
                program_id=program_record.id, expiry_date__isnull=True
            )

            record.team_members.set(team_members)

            return record

        except models.Program.DoesNotExist as exc:
            err_msg = f"Program (pa_number={pa_number}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.ProgramReviewToolError(err_msg, 404) from exc

    @staticmethod
    def fetch_record(
        pa_number: str, reporting_period: int, refresh: bool = False
    ) -> dict:
        """
        Fetch the `Program` record data for the given reporting period
        and PA number.

        Accepts:
            * pa_number (str): PA number of related `Program` record whose
                reporting period `Record` is being retrieved.
            * reporting_period (int): The reporting period (e.g., `202306`
                for June 2023).
            * refresh (bool): Optional flag to indicate if the program
                metrics data should be sourced from the `Program` record
                (which will be kept up to date from external source syncing),
                or not.

        Returns:
            * record_data (dict): A `Program`'s record data for the given
                reporting period.
        """

        try:
            # If no `Program` PA number is given, throw an error.
            if not pa_number:
                err_msg = "Missing PA number."
                LOGGER.error(err_msg)
                raise exceptions.ProgramReviewToolError(err_msg, 400)

            # If no reporting period is given, throw an error.
            if not reporting_period:
                err_msg = "No reporting period given."
                LOGGER.error(err_msg)
                raise exceptions.ProgramReviewToolError(err_msg, 400)

            # Fetch `Program` record.
            program: models.Program = models.Program.objects.get(pa_number=pa_number)

            # Retrieve all `Record`s for the `Program`.
            records_for_program: QuerySet[models.Record] = models.Record.objects.filter(
                program=program
            )

            # Get the most recent `Record`, for the given reporting period.
            latest_record_for_reporting_period: Union[models.Record, None] = (
                records_for_program.filter(reporting_period=reporting_period)
                .order_by("id")
                .last()
            )

            # Serialize the `Program`s data.
            program_data: dict = ProgramSerializer(program).data

            # If `latest_record_for_reporting_period` is not None, then
            # serialize it and assign its data.
            latest_record_for_reporting_period_data: dict = (
                RecordSerializer(latest_record_for_reporting_period).data
                if latest_record_for_reporting_period is not None
                else {}
            )

            # Set the source to be used for program metrics
            # data points. If the `latest_record_for_reporting_period`
            # is None or the `refresh` flag is True, then set
            # the source to the `program_data` else set
            # it to the `latest_record_for_reporting_period_data`.
            source_for_program_metrics_data: dict = (
                program_data
                if latest_record_for_reporting_period is None or refresh
                else latest_record_for_reporting_period_data
            )

            # Dictionary containing the program metrics data.
            program_metrics_data: dict = {**DEFAULT_PROGRAM_METRICS_DATA}

            # Loop through the `program_metrics_data` keys, and
            # assign the values found in `source_for_program_metrics_data`.
            for program_metric in program_metrics_data:
                program_metrics_data[program_metric] = source_for_program_metrics_data[
                    program_metric
                ]

            # In the event that the `latest_record_for_reporting_period` is not None,
            # proceed to query for the most recent `Record` for a previous reporting
            # period.
            previous_period_most_recent_record: Union[models.Record, None] = (
                None
                if latest_record_for_reporting_period is not None
                else records_for_program.filter(reporting_period__lt=reporting_period)
                .order_by("id")
                .last()
            )

            # If the `previous_period_most_recent_record` is not None, then
            # serialize it and assign its data.
            previous_period_most_recent_record_data: dict = (
                RecordSerializer(previous_period_most_recent_record).data
                if previous_period_most_recent_record is not None
                else {}
            )

            # Source for shared `Record` data. These data points
            # can either be sourced from: `latest_record_for_reporting_period_data`
            # (if it exists/is not empty) or from:
            # previous_period_most_recent_record_data`.
            source_for_shared_record_metrics_data: dict = (
                latest_record_for_reporting_period_data
                if latest_record_for_reporting_period_data
                else previous_period_most_recent_record_data
            )

            # Dictionary containing the shared `Record` metrics data.
            shared_record_metrics_data: dict = {**DEFAULT_SHARED_RECORD_METRICS_DATA}

            # Loop through the `shared_record_metrics_data` keys, and
            # assign the values found in `source_for_shared_record_metrics_data`,
            # if the key exists.
            for shared_record_metric in shared_record_metrics_data:
                if shared_record_metric in source_for_shared_record_metrics_data:
                    shared_record_metrics_data[
                        shared_record_metric
                    ] = source_for_shared_record_metrics_data[shared_record_metric]

            # Dictionary containing the current period's `Record` metrics data.
            current_period_metrics_data: dict = {
                **DEFAULT_CURRENT_PERIOD_RECORD_METRICS_DATA
            }
            # Loop through the `current_period_metrics_data` keys, and
            # assign the values found in `latest_record_for_reporting_period_data`,
            # if the key exists.
            for current_period_metric in current_period_metrics_data:
                if current_period_metric in latest_record_for_reporting_period_data:
                    current_period_metrics_data[
                        current_period_metric
                    ] = latest_record_for_reporting_period_data[current_period_metric]

            # Set the `Record` id value to placed in the
            # `record_data`. This id will be the id of the
            # `latest_record_for_reporting_period` if it is
            # not None and if `refresh` is False.
            record_id: Union[int, None] = (
                latest_record_for_reporting_period.id
                if latest_record_for_reporting_period is not None and not refresh
                else None
            )

            # Merge all data the in the three dictionaries containing
            # the `Program`s record data into one.
            record_data = {
                "id": record_id,
                "reporting_period": reporting_period,
                **program_metrics_data,
                **shared_record_metrics_data,
                **current_period_metrics_data,
            }

            return record_data
        except models.Program.DoesNotExist as exc:
            err_msg = f"Program (pa_number={pa_number}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.ProgramReviewToolError(err_msg, 404) from exc
