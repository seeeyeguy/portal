"""
Collection of pytests for Usage's create controller.
"""

# pylint: disable=wrong-import-order
import pytest
from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag

from program_review_tool import controllers, exceptions, models
from program_review_tool.controllers.Usage.tests.mutations.create.default import (
    arguments,
)
from program_review_tool.models.Usage.serializers import UsageSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "usage",
    "program_review_tool",
    "controllers.TestCreateUsage",
    "program_review_tool.usage.create",
    "usage.create.default",
)
class TestCreateUsage(MultiDBTestCase):
    """Test suite for Usage's create controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/users/users.json",
    ]

    @tag("controllers.usage.create_usage")
    def test_create_usage(self) -> None:
        """Success Case: Create a `Usage` record."""

        # Query user from database.
        user = AuthModels.User.objects.get(username=arguments.CREATE_USAGE_USER_EMAIL)

        # Create usage for generation.
        usage = controllers.Usage.create_usage(
            user=user.email,
            programs=arguments.CREATE_USAGE_PROGRAM_PAS,
        )

        # Ensure data is a `Usage` instance.
        self.assertIsInstance(usage, models.Usage)

        data: dict = UsageSerializer(usage).data

        del data["created"]

        # Ensure data is correct.
        self.assertDictEqual(data, arguments.CREATE_USAGE_EXPECTED_USAGE)

    @tag("controllers.usage.create_usage_user_dne")
    def test_create_usage_user_dne(self) -> None:
        """Fail Case: Create a `Usage` record with a `User`
        that does not exist."""

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Usage.create_usage(
                user=arguments.CREATE_USAGE_USER_EMAIL_DNE,
                programs=arguments.CREATE_USAGE_PROGRAM_PAS,
            )
