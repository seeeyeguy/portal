"""
Collection of pytests for ReportingPeriod's fetch controller.
"""

# pylint: disable=wrong-import-order
import pytest
from typing import List

from django.test import tag

from program_review_tool import controllers
from program_review_tool.controllers.ReportingPeriod.tests.query.read.collection import (
    arguments,
)

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "program_review_tool",
    "reporting_period",
    "controllers.TestFetchReportingPeriod",
    "program_review_tool.reporting_period.fetch",
    "reporting_period.fetch.serialized",
)
class TestFetchReportingPeriod(MultiDBTestCase):
    """Test suite for ReportingPeriod's fetch controller."""

    @tag("controllers.reporting_period.fetch_reporting_period")
    def test_fetch_reporting_period(self) -> None:
        """Success: Fetch the current reporting period."""

        reporting_periods: List[
            int
        ] = controllers.ReportingPeriod.fetch_reporting_periods(
            previous_period_count=None
        )

        self.assertListEqual(
            reporting_periods,
            arguments.FETCH_REPORTING_PERIOD_EXPECTED_REPORTING_PERIODS,
        )

    @tag(
        "controllers.reporting_period.fetch_reporting_period_with_previous_period_count"
    )
    def test_fetch_reporting_period_with_previous_period_count(self) -> None:
        """Success: Fetch the current reporting period with previous
        reporting count to include previous periods."""

        reporting_periods: List[
            int
        ] = controllers.ReportingPeriod.fetch_reporting_periods(
            previous_period_count=arguments.FETCH_REPORTING_PERIOD_WITH_PREVIOUS_PERIOD_COUNT_COUNT
        )

        self.assertListEqual(
            reporting_periods,
            arguments.FETCH_REPORTING_PERIOD_WITH_PREVIOUS_PERIOD_COUNT_EXPECTED_REPORTING_PERIODS,
        )
