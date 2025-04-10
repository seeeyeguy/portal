"""
Collection of pytests for Programs's review view endpoint.
"""

from django.test import tag
from django.urls import reverse

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

    url: str = reverse("program_review_tool.program")

    @tag("views.program.review_programs_by_program_ids")
    def test_fetch_programs_by_program_ids(self) -> None:
        """Success Case: Review `Program` records for
        the given ids."""

    @tag("views.program.review_programs_by_program_ids_dne")
    def test_review_programs_by_program_ids_dne(self) -> None:
        """Fail Case: Review `Program` records for
        ids that do not exist."""

    @tag("views.program.review_programs_user_dne")
    def test_review_programs_user_dne(self) -> None:
        """Fail Case: Review `Program` records for a `User`
        that does not exist."""

    @tag("views.program.review_programs_empty_name")
    def test_review_programs_empty_name(self) -> None:
        """Fail Case: Review `Program` records with an empty
        given name."""
