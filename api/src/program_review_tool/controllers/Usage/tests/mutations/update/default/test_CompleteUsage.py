"""
Collection of pytests for Usage's update controller.
"""

import pytest
import pytz
from typing import List
from datetime import datetime

from django.test import tag

from program_review_tool import controllers, exceptions, models
from program_review_tool.controllers.Usage.tests.mutations.update.default import (
    arguments,
)
from program_review_tool.models.Usage.serializers import UsageSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "program_review_tool",
    "usage",
    "controllers.TestUpdateUsage",
    "program_review_tool.usage.update",
    "program_review_tool.usage.update.default",
)
class TestUpdateUsage(MultiDBTestCase):
    """Test suite for Usage's update controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Usage/tests/mutations/update/default/fixtures/usages.json",
    ]

    @tag("controllers.usage.complete_usage")
    def test_complete_usage(self) -> None:
        """Success Case: Complete a `Usage` record."""

        # Parse the datetime string to a datetime object.
        finish_time_naive = datetime.strptime(
            arguments.COMPLETE_USAGE_FINISH_TIME, "%Y-%m-%dT%H:%M:%SZ"
        )

        # Make the `finish_time`` timezone-aware.
        finish_time = pytz.UTC.localize(finish_time_naive)

        # Complete `Usage` record.
        usage = controllers.Usage.complete_usage(
            usage_id=arguments.COMPLETE_USAGE_ID, success=True, finish_time=finish_time
        )

        self.assertIsInstance(usage, models.Usage)

        # Serialize `Usage`.
        data = UsageSerializer(usage).data

        self.assertEqual(data, arguments.COMPLETE_USAGE_EXPECTED_USAGE)

    @tag("controllers.usage.complete_usage_already_completed")
    def test_complete_usage_already_completed(self) -> None:
        """Success Case: Complete a `Usage` record that already completed."""

        # Parse the datetime string to a datetime object.
        finish_time_naive = datetime.strptime(
            arguments.COMPLETE_USAGE_FINISH_TIME, "%Y-%m-%dT%H:%M:%SZ"
        )

        # Make the `finish_time` timezone-aware.
        finish_time = pytz.UTC.localize(finish_time_naive)

        # Complete `Usage` record.
        usage = controllers.Usage.complete_usage(
            usage_id=arguments.COMPLETE_USAGE_ID_ALREADY_COMPLETED,
            success=True,
            finish_time=finish_time,
        )

        self.assertIsInstance(usage, models.Usage)

        # Serialize `Usage`.
        data = UsageSerializer(usage).data

        self.assertEqual(
            data, arguments.COMPLETE_USAGE_ALREADY_COMPLETED_EXPECTED_USAGE
        )

    @tag("controllers.usage.complete_usage_record_dne")
    def test_complete_usage_record_dne(self) -> None:
        """Fail Case: Complete a `Usage` that does not exist."""

        # Parse the datetime string to a datetime object.
        finish_time_naive = datetime.strptime(
            arguments.COMPLETE_USAGE_FINISH_TIME, "%Y-%m-%dT%H:%M:%SZ"
        )

        # Make the `finish_time` timezone-aware.
        finish_time = pytz.UTC.localize(finish_time_naive)

        with pytest.raises(exceptions.ProgramReviewToolError):
            _ = controllers.Usage.complete_usage(
                usage_id=arguments.COMPLETE_USAGE_ID_DNE,
                success=True,
                finish_time=finish_time,
            )
