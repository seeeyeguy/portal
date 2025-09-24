"""
`Program Review Tool` reporting period data fetch utils module. Common
functionality for the `Program Review Tool` `Reporting` app to help
with retrieving reporting period data from the external FDW database
source.
"""

import logging
from typing import List

from sqlalchemy.exc import DatabaseError, OperationalError

from program_review_tool.models.Program.utils import (
    AcceptedExternalDatabases,
    ExternalDatabaseConnector,
)

from manager.settings import ApplicationBuild, BUILD

LOGGER = logging.getLogger(__name__)

TEST_REPORTING_PERIODS: List[int] = [202505, 202504, 202503, 202502, 202501]


def get_reporting_periods_from_external_source() -> List[int]:
    """
    Returns a list of reporting periods (e.g., `202306` for June 2023),
    retrieved from an external database source, ordered in descending
    order.

    Accepts:
        * None

    Returns:
        * reporting_periods (List[int]) List of (e.g., `202306` for June 2023),
            retrieved from an external database source, ordered in descending
            order.
    """

    # If the `BUILD` is equal to `test` then return the `TEST_REPORTING_PERIODS`.
    if BUILD == ApplicationBuild.TEST:
        return TEST_REPORTING_PERIODS

    try:

        # SQL statement that retrieves the reporting periods in descending
        # order.
        sql: str = """
            SELECT DISTINCT FISCAL_YEARMO_PRIOR
            FROM BUSANA.DIM_DATE
            WHERE FULL_DATE <= TRUNC(SYSDATE)
            ORDER BY BUSANA.DIM_DATE.FISCAL_YEARMO_PRIOR DESC
        """

        # Get connection to external database source.
        conn = ExternalDatabaseConnector(AcceptedExternalDatabases.FDW)

        # Query the external source.
        df = conn.query_db(sql)

        # Place query results in a list.
        reporting_periods: List[int] = list(df["fiscal_yearmo_prior"])

        return reporting_periods
    except DatabaseError as exc:
        err_msg = f"""
            The following error: {exc}, occurred while fetching reporting
            periods from external source.
            """
        LOGGER.error(err_msg)
        return []
