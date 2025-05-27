"""
Collection of pytests for Programs's review view endpoint.
"""

from typing import List
from rest_framework import status

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse

from program_review_tool.controllers.Program.tests.mutations.create.default import (
    arguments,
)
from program_review_tool.utils.review.export import ExportStatus

from manager.utils.tests import MultiDBTestCase


@tag(
    "program",
    "program_review_tool",
    "views",
    "program.review.default",
    "program_review_tool.program.review",
    "views.TestReviewProgram",
)
class TestReviewProgram(MultiDBTestCase):
    """
    Tests for POST /v1/program-review-tool/program/review endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Program/tests/mutations/create/default/fixtures/segments.json",
        "program_review_tool/controllers/Program/tests/mutations/create/default/fixtures/programs.json",
    ]

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(
            email=arguments.CREATE_PROGRAMS_REVIEW_USER_EMAIL
        )
        self.client.force_login(user=user)

    url: str = reverse("program_review_tool.program")

    @tag("views.program.create_programs_review_by_program_ids")
    def test_create_programs_review_by_program_ids(self) -> None:
        """Success Case: Create `Program`s Review for
        the given ids."""

        body: dict = {
            "programs": arguments.CREATE_PROGRAMS_REVIEW_PROGRAM_IDS,
            "name": arguments.CREATE_PROGRAMS_REVIEW_PROGRAM_NAME,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        review_status = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(review_status, ExportStatus.QUEUED)

    @tag("views.program.create_programs_review_by_program_ids_empty")
    def test_create_programs_review_by_program_ids_empty(self) -> None:
        """Fail Case: Create `Program`s Review, supplying
        an empty ids list."""

        body: dict = {
            "programs": [],
            "name": arguments.CREATE_PROGRAMS_REVIEW_PROGRAM_NAME,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.program.create_programs_review_empty_review_name")
    def test_create_programs_review_empty_review_name(self) -> None:
        """Fail Case: Create `Program`s Review with an empty
        review name."""

        body: dict = {
            "programs": arguments.CREATE_PROGRAMS_REVIEW_PROGRAM_IDS,
            "name": "",
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.program.create_programs_review_by_program_ids_dne")
    def test_create_programs_review_by_program_ids_dne(self) -> None:
        """Fail Case: Create `Program`s Review with ids
        for Programs that do not exist."""

        body: dict = {
            "programs": arguments.CREATE_PROGRAMS_REVIEW_PROGRAM_IDS_DNE,
            "name": arguments.CREATE_PROGRAMS_REVIEW_PROGRAM_NAME,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
