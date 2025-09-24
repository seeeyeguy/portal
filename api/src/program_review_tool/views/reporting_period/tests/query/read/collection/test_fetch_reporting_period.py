"""
Collection of pytests for ReportingPeriod's fetch view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from program_review_tool.controllers.ReportingPeriod.tests.query.read.collection import (
    arguments,
)

from manager.utils.tests import MultiDBTestCase


@tag(
    "views",
    "reporting_period",
    "program_review_tool",
    "reporting_period.fetch.serialized",
    "program_review_tool.reporting_period.fetch",
    "views.TestFetchReportingPeriod",
)
class TestFetchReportingPeriod(MultiDBTestCase):
    """
    Tests for GET /v1/program-review-tool/reporting-period endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/users/users.json",
    ]

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(email=arguments.FETCH_REPORTING_USER_EMAIL)
        self.client.force_login(user=user)

    url: str = reverse("program_review_tool.reporting_period")

    @tag("views.reporting_period.fetch_reporting_period")
    def test_fetch_reporting_period(self) -> None:
        """Success: Fetch the current reporting period."""

        response = self.client.get(
            self.url, headers={"content_type": "application/json"}
        )

        reporting_periods = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertListEqual(
            reporting_periods,
            arguments.FETCH_REPORTING_PERIOD_EXPECTED_REPORTING_PERIODS,
        )

    @tag("views.reporting_period.fetch_reporting_period_with_previous_period_count")
    def test_fetch_reporting_period_with_previous_period_count(self) -> None:
        """Success: Fetch the current reporting period with previous
        reporting count to include previous periods."""

        params: dict = {
            "previous_period_count": arguments.FETCH_REPORTING_PERIOD_WITH_PREVIOUS_PERIOD_COUNT_COUNT
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        reporting_periods = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertListEqual(
            reporting_periods,
            arguments.FETCH_REPORTING_PERIOD_WITH_PREVIOUS_PERIOD_COUNT_EXPECTED_REPORTING_PERIODS,
        )
