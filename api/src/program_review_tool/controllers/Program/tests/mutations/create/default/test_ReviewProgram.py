"""
Collection of pytests for Program's review controller.
"""

# pylint: disable=line-too-long,wrong-import-order
import pytest
from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag

from program_review_tool import controllers, exceptions, models
from program_review_tool.controllers.Program.tests.mutations.create.default import (
    arguments,
)
from program_review_tool.utils.review.export import ExportStatus

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "program",
    "program_review_tool",
    "controllers.TestReviewProgram",
    "program.review.default",
    "program_review_tool.program.review",
)
class TestReviewProgram(MultiDBTestCase):
    """Test suite for Program's review controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Program/tests/mutations/create/default/fixtures/segments.json",
        "program_review_tool/controllers/Program/tests/mutations/create/default/fixtures/programs.json",
    ]

    @tag("controllers.program.create_programs_review_by_program_ids")
    def test_create_programs_review_by_program_ids(self) -> None:
        """Success Case: Create `Program`s Review for
        the given ids."""

        user = AuthModels.User.objects.get(
            username=arguments.CREATE_PROGRAMS_REVIEW_USER_EMAIL
        )

        review_status, review_path = controllers.Program.review_programs(
            program_ids=arguments.CREATE_PROGRAMS_REVIEW_PROGRAM_IDS,
            user=user,
            review_name=arguments.CREATE_PROGRAMS_REVIEW_PROGRAM_NAME,
        )

        self.assertEqual(review_status, ExportStatus.QUEUED)
        self.assertIsNone(review_path)

    @tag("controllers.program.create_programs_review_by_program_ids_empty")
    def test_create_programs_review_by_program_ids_empty(self) -> None:
        """Fail Case: Create `Program`s Review, supplying
        an empty ids list."""

        user = AuthModels.User.objects.get(
            username=arguments.CREATE_PROGRAMS_REVIEW_USER_EMAIL
        )
        with pytest.raises(exceptions.ProgramReviewToolError):
            _ = controllers.Program.review_programs(
                program_ids=[],
                user=user,
                review_name=arguments.CREATE_PROGRAMS_REVIEW_PROGRAM_NAME,
            )

    @tag("controllers.program.create_programs_review_empty_review_name")
    def test_create_programs_review_empty_review_name(self) -> None:
        """Fail Case: Create `Program`s Review with an empty
        review name."""

        user = AuthModels.User.objects.get(
            username=arguments.CREATE_PROGRAMS_REVIEW_USER_EMAIL
        )
        with pytest.raises(exceptions.ProgramReviewToolError):
            _ = controllers.Program.review_programs(
                program_ids=arguments.CREATE_PROGRAMS_REVIEW_PROGRAM_IDS,
                user=user,
                review_name="",
            )

    @tag("controllers.program.create_programs_review_by_program_ids_dne")
    def test_create_programs_review_by_program_ids_dne(self) -> None:
        """Fail Case: Create `Program`s Review with ids
        for Programs that do not exist."""

        user = AuthModels.User.objects.get(
            username=arguments.CREATE_PROGRAMS_REVIEW_USER_EMAIL
        )
        with pytest.raises(exceptions.ProgramReviewToolError):
            _ = controllers.Program.review_programs(
                program_ids=arguments.CREATE_PROGRAMS_REVIEW_PROGRAM_IDS_DNE,
                user=user,
                review_name=arguments.CREATE_PROGRAMS_REVIEW_PROGRAM_NAME,
            )
