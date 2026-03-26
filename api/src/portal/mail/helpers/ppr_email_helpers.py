import calendar
import logging
from datetime import datetime
from sqlalchemy.exc import DatabaseError

from django.db.models import Q

from content.controllers.Content import Content
from program_review_tool.models.Program import Program
from program_review_tool.models.Program.utils import (
    AcceptedExternalDatabases,
    ExternalDatabaseConnector,
)
from program_review_tool.models.ProgramMember import ProgramMember
from program_review_tool.models.Record import Record


def days_until_next_month() -> int:
    """
    Calculates the number of days from today until the first of the next month.

    Accepts:
        * None

    Returns:
        * (int): Number of days until next month.
    """

    today = datetime.today()
    last_day = calendar.monthrange(today.year, today.month)[1]

    return last_day + 1 - today.day


def get_current_reporting_period():
    """
    Fetches the PPR manually set reporting periods in a list and returns the current reporting
    period.

    Accepts:
        * None

    Returns:
        * (int): The reporting period (e.g., `202306` for June 2023).
    """

    reporting_period_content = Content.fetch_content("ADMIN_REPORTING_PERIOD_PPR")
    if reporting_period_content and reporting_period_content.content:
        reporting_periods = reporting_period_content.content.get("periods", [])
        if reporting_periods and len(reporting_periods) > 0:
            return reporting_periods[0]

    return None


def get_period_fdw(date: datetime, offset: int) -> int:
    """
    Fetch the reporting period from an external database source at offset periods away from the
    given date.

    Accepts:
        * date (datetime): The date that a reporting period falls in.
        * offset (int): The number of periods away from the period that date falls in, where 0
            is the current period.

    Returns:
        * (int): The period at offset (e.g., `202306` for June 2023).
    """

    LOGGER = logging.getLogger(__name__)

    date_str = date.strftime("%Y-%m-%d")
    try:
        # SQL statement that retrieves the reporting periods in descending
        # order.
        sql: str = f"""
            SELECT DISTINCT FISCAL_YEARMO_PRIOR
            FROM BUSANA.DIM_DATE
            WHERE FULL_DATE <= TO_DATE("{date_str}", "YYYY-MM-DD")
            ORDER BY BUSANA.DIM_DATE.FISCAL_YEARMO_PRIOR DESC
        """

        conn = ExternalDatabaseConnector(AcceptedExternalDatabases.FDW)
        if conn is None or not conn.is_connected():
            raise ConnectionError("Failed to connect to database.")

        df = conn.query_db(sql)
        if df.empty:
            raise ValueError("No data returned from the query.")

        reporting_periods = list(df["fiscal_yearmo_prior"])

        if not reporting_periods:
            return None
        if len(reporting_periods) < offset + 1:
            return None
        return reporting_periods[offset]

    except ConnectionError as exc:
        conn_err = f"""
            The following error: {exc}, occurred while connecting to
            an external database.
            """
        LOGGER.error(conn_err)
    except ValueError as exc:
        val_err = f"""
            The following error: {exc}, occurred while querying an
            external database.
            """
        LOGGER.error(val_err)
    except DatabaseError as exc:
        err_msg = f"""
            The following error: {exc}, occurred while fetching reporting
            periods from external source.
            """
        LOGGER.error(err_msg)

    return None


def is_overdue() -> list:
    """
    Fetches the current reporting period and determines whether today is two months past that date
    (overdue). Also returns the current reporting period and the month of the due date.

    Accepts:
        * None

    Returns:
        * (list): A list containing:
            - (bool): whether today is past due
            - (list: [int, int]): current reporting period year, month
            - (str): month of the due date
    """

    current_reporting_period = get_current_reporting_period()
    if not current_reporting_period:
        current_reporting_period = get_period_fdw(datetime.today(), 1)
    if not current_reporting_period:
        raise ValueError("Could not fetch current reporting period.")
    period_month = int(str(current_reporting_period)[4:])
    period_year = int(str(current_reporting_period)[:4])

    # Due date is two months after the current reporting period
    month = period_month + 2
    year = period_year
    if month > 12:
        month %= 12
        year += 1
    due_date = datetime(int(year), int(month), 1)

    today = datetime.today()

    # Calculate difference in number of months between today and due date
    if (today.year - due_date.year) * 12 + (today.month - due_date.month) >= 0:
        return [True, [period_year, period_month], due_date]

    return [False, [period_year, period_month], calendar.month_name[due_date.month]]


def find_missing_programs() -> list:
    """
    Fetches a list of reportable `Program`s (active and tier 1/2) with a missing `Record` in the
    current reporting period.

    Accepts:
        * None

    Returns:
        * missing_programs (list): Reportable `Program`s without a `Record` in the current
            reporting period.
    """

    current_reporting_period = get_current_reporting_period()
    if not current_reporting_period:
        current_reporting_period = get_period_fdw(datetime.today(), 1)
    if not current_reporting_period:
        raise ValueError("Could not fetch current reporting period.")

    reportable_programs = Program.objects.filter(
        active_status=True, tier__in=[1, 2], segment__in=[1, 5]
    )

    programs_with_records = Record.objects.filter(
        program__in=reportable_programs, reporting_period=current_reporting_period
    ).values_list("program", flat=True)

    missing_programs = reportable_programs.exclude(
        id__in=programs_with_records
    ).distinct()

    return missing_programs


def find_members_programs() -> dict:
    """
    Creates a dictionary of `User`s and their programs with missing `Record`s in the current
    reporting period.

    Accepts:
        * None

    Returns:
        * member_to_programs (dict): `User`s and their programs with missing `Record`s
    """

    member_to_programs = {}
    missing_programs = find_missing_programs()

    program_members = ProgramMember.objects.filter(
        program__in=missing_programs, expiry_date=None
    ).select_related("user", "program")

    for member in program_members:
        user = member.user
        member_to_programs.setdefault(user, []).append(member.program.name)

    return member_to_programs