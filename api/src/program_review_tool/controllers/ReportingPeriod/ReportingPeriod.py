"""
`BI Portal` `ReportingPeriod` controller module.
"""

from typing import List, Optional

from program_review_tool.utils.reporting_period.fetch import (
    get_reporting_periods_from_external_source,
)


MINIMUM_NUMBER_OF_REPORTING_PERIODS: int = 1


class ReportingPeriod:
    """
    Container class for functions related to retrieving reporting
    periods (e.g., `202306` for June 2023) from an external database
    source.
    """

    @staticmethod
    def fetch_reporting_periods(previous_period_count: Optional[int] = 0) -> List[int]:
        """
        Fetch a list of reporting periods (list begins with the current
        reporting period) from an external database source.

        Accepts:
            * previous_period_count (Optional[int]): Number of previous reporting
                periods to include in the results.

        Returns:
            * reporting_periods (List[int]): A list containing the retrieved
                reporting periods (list begins with the current reporting
                period) from the external database source.
        """

        number_of_reporting_periods: int = (
            MINIMUM_NUMBER_OF_REPORTING_PERIODS
            if previous_period_count is None or previous_period_count < 0
            else previous_period_count + MINIMUM_NUMBER_OF_REPORTING_PERIODS
        )

        reporting_periods: List[int] = get_reporting_periods_from_external_source()

        return reporting_periods[:number_of_reporting_periods]
