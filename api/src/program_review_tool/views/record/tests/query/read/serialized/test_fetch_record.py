"""
Collection of pytests for Record's fetch view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from program_review_tool.controllers.Record.tests.query.read.serialized import (
    arguments,
)

from manager.utils.tests import MultiDBTestCase


@tag(
    "record",
    "program_review_tool",
    "views",
    "record.fetch.serialized",
    "program_review_tool.record.fetch",
    "views.TestFetchRecord",
)
class TestFetchRecord(MultiDBTestCase):
    """
    Tests for GET /v1/program-review-tool/record endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Record/tests/query/read/serialized/fixtures/programs.json",
        "program_review_tool/controllers/Record/tests/query/read/serialized/fixtures/program_members.json",
        "program_review_tool/controllers/Record/tests/query/read/serialized/fixtures/records.json",
    ]

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(email=arguments.FETCH_RECORD_USER_EMAIL)
        self.client.force_login(user=user)

    url: str = reverse("program_review_tool.record")

    @tag("views.record.fetch_record")
    def test_fetch_record(self) -> None:
        """Success: Fetch `Record` record for `Program`
        and reporting period."""

        params: dict = {
            "pa_number": arguments.FETCH_RECORD_PROGRAM_PA_NUMBER,
            "reporting_period": arguments.FETCH_RECORD_REPORTING_PERIOD,
            "refresh": False,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        record_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(record_data, arguments.FETCH_RECORD_EXPECTED_RECORD_DATA)

    @tag("views.record.fetch_record_no_current_record_for_reporting_period")
    def test_fetch_record_no_current_record_for_reporting_period(self) -> None:
        """Success: Fetch `Record` record for `Program`
        and reporting period, where there does not exist
        a `Record` for the supplied reporting period, but
        there exists a `Record` for a previous reporting
        period"""

        params: dict = {
            "pa_number": arguments.FETCH_RECORD_PROGRAM_PA_NUMBER,
            "reporting_period": arguments.FETCH_RECORD_NO_CURRENT_RECORD_FOR_REPORTING_PERIOD_REPORTING_PERIOD,
            "refresh": False,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        record_data = response.json()

        for obj in record_data["team_members"]:
            obj.get("role", {}).pop("created", None)
            obj.get("role", {}).pop("modified", None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            record_data,
            arguments.FETCH_RECORD_NO_CURRENT_RECORD_FOR_REPORTING_PERIOD_EXPECTED_RECORD_DATA,
        )

    @tag("views.record.fetch_record_no_record_exists_for_program")
    def test_fetch_record_no_record_exists_for_program(self) -> None:
        """Success: Fetch `Record` record for `Program`
        and reporting period, where there does not exist
        a `Record` for the supplied `Program` and reporting
        period."""

        params: dict = {
            "pa_number": arguments.FETCH_RECORD_NO_EXISTING_RECORD_PROGRAM_PA_NUMBER,
            "reporting_period": arguments.FETCH_RECORD_REPORTING_PERIOD,
            "refresh": False,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        record_data = response.json()

        for obj in record_data["team_members"]:
            obj.get("role", {}).pop("created", None)
            obj.get("role", {}).pop("modified", None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            record_data,
            arguments.FETCH_RECORD_NO_EXISTING_RECORD_EXPECTED_RECORD_DATA,
        )

    @tag("views.record.fetch_record_with_refresh")
    def test_fetch_record_with_refresh(self) -> None:
        """Success: Fetch `Record` record for `Program`
        and reporting period, with refresh flag set
        to True."""

        params: dict = {
            "pa_number": arguments.FETCH_RECORD_PROGRAM_PA_NUMBER,
            "reporting_period": arguments.FETCH_RECORD_REPORTING_PERIOD,
            "refresh": True,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        record_data = response.json()

        for obj in record_data["team_members"]:
            obj.get("role", {}).pop("created", None)
            obj.get("role", {}).pop("modified", None)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            record_data,
            arguments.FETCH_RECORD_WITH_REFRESH_EXPECTED_RECORD_DATA,
        )

    @tag("views.record.fetch_record_empty_pa_number")
    def test_fetch_record_empty_pa_number(self) -> None:
        """Fail Case: Fetch `Record` record with an empty
        PA number."""

        params: dict = {
            "pa_number": "",
            "reporting_period": arguments.FETCH_RECORD_REPORTING_PERIOD,
            "refresh": False,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.record.fetch_record_program_dne")
    def test_fetch_record_program_dne(self) -> None:
        """Fail Case: Fetch `Record` record with a `Program`
        that does not exist."""

        params: dict = {
            "pa_number": arguments.FETCH_RECORD_PROGRAM_PA_NUMBER_DNE,
            "reporting_period": arguments.FETCH_RECORD_REPORTING_PERIOD,
            "refresh": False,
        }

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
