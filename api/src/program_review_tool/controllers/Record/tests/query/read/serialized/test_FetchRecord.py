"""
Collection of pytests for Record's fetch controller.
"""

# pylint: disable=wrong-import-order
import pytest
from typing import List

from django.test import tag

from program_review_tool import controllers, exceptions
from program_review_tool.controllers.Record.tests.query.read.serialized import arguments

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "program_review_tool",
    "record",
    "controllers.TestFetchRecord",
    "program_review_tool.record.fetch",
    "record.fetch.serialized",
)
class TestFetchRecord(MultiDBTestCase):
    """Test suite for Record's fetch controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Record/tests/query/read/serialized/fixtures/programs.json",
        "program_review_tool/controllers/Record/tests/query/read/serialized/fixtures/program_members.json",
        "program_review_tool/controllers/Record/tests/query/read/serialized/fixtures/records.json",
    ]

    @tag("controllers.record.fetch_record")
    def test_fetch_record(self) -> None:
        """Success: Fetch `Record` record for `Program`
        and reporting period."""

        record_data: dict = controllers.Record.fetch_record(
            pa_number=arguments.FETCH_RECORD_PROGRAM_PA_NUMBER,
            reporting_period=arguments.FETCH_RECORD_REPORTING_PERIOD,
            refresh=False,
        )

        self.assertDictEqual(record_data, arguments.FETCH_RECORD_EXPECTED_RECORD_DATA)

    @tag("controllers.record.fetch_record_no_current_record_for_reporting_period")
    def test_fetch_record_no_current_record_for_reporting_period(self) -> None:
        """Success: Fetch `Record` record for `Program`
        and reporting period, where there does not exist
        a `Record` for the supplied reporting period, but
        there exists a `Record` for a previous reporting
        period"""

        record_data: dict = controllers.Record.fetch_record(
            pa_number=arguments.FETCH_RECORD_PROGRAM_PA_NUMBER,
            reporting_period=arguments.FETCH_RECORD_NO_CURRENT_RECORD_FOR_REPORTING_PERIOD_REPORTING_PERIOD,
            refresh=False,
        )

        for obj in record_data["team_members"]:
            obj.get("role", {}).pop("created", None)
            obj.get("role", {}).pop("modified", None)

        self.assertDictEqual(
            record_data,
            arguments.FETCH_RECORD_NO_CURRENT_RECORD_FOR_REPORTING_PERIOD_EXPECTED_RECORD_DATA,
        )

    @tag("controllers.record.fetch_record_no_record_exists_for_program")
    def test_fetch_record_no_record_exists_for_program(self) -> None:
        """Success: Fetch `Record` record for `Program`
        and reporting period, where there does not exist
        a `Record` for the supplied `Program` and reporting
        period."""

        record_data: dict = controllers.Record.fetch_record(
            pa_number=arguments.FETCH_RECORD_NO_EXISTING_RECORD_PROGRAM_PA_NUMBER,
            reporting_period=arguments.FETCH_RECORD_REPORTING_PERIOD,
            refresh=False,
        )

        for obj in record_data["team_members"]:
            obj.get("role", {}).pop("created", None)
            obj.get("role", {}).pop("modified", None)

        self.assertDictEqual(
            record_data,
            arguments.FETCH_RECORD_NO_EXISTING_RECORD_EXPECTED_RECORD_DATA,
        )

    @tag("controllers.record.fetch_record_with_refresh")
    def test_fetch_record_with_refresh(self) -> None:
        """Success: Fetch `Record` record for `Program`
        and reporting period, with refresh flag set
        to True."""

        record_data: dict = controllers.Record.fetch_record(
            pa_number=arguments.FETCH_RECORD_PROGRAM_PA_NUMBER,
            reporting_period=arguments.FETCH_RECORD_REPORTING_PERIOD,
            refresh=True,
        )

        for obj in record_data["team_members"]:
            obj.get("role", {}).pop("created", None)
            obj.get("role", {}).pop("modified", None)

        self.assertDictEqual(
            record_data,
            arguments.FETCH_RECORD_WITH_REFRESH_EXPECTED_RECORD_DATA,
        )

    @tag("controllers.record.fetch_record_empty_pa_number")
    def test_fetch_record_empty_pa_number(self) -> None:
        """Fail Case: Fetch `Record` record with an empty
        PA number."""

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Record.fetch_record(
                pa_number="",
                reporting_period=arguments.FETCH_RECORD_REPORTING_PERIOD,
                refresh=False,
            )

    @tag("controllers.record.fetch_record_null_reporting_period")
    def test_fetch_record_null_reporting_period(self) -> None:
        """Fail Case: Fetch `Record` record with a null
        reporting period."""

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Record.fetch_record(
                pa_number=arguments.FETCH_RECORD_PROGRAM_PA_NUMBER,
                reporting_period=None,  # type: ignore[arg-type]
                refresh=False,
            )

    @tag("controllers.record.fetch_record_program_dne")
    def test_fetch_record_program_dne(self) -> None:
        """Fail Case: Fetch `Record` record with a `Program`
        that does not exist."""

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Record.fetch_record(
                pa_number=arguments.FETCH_RECORD_PROGRAM_PA_NUMBER_DNE,
                reporting_period=arguments.FETCH_RECORD_REPORTING_PERIOD,
                refresh=False,
            )
