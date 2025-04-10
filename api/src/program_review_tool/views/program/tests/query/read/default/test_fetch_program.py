"""
Collection of pytests for Programs's fetch view endpoint.
"""

from django.test import tag
from django.urls import reverse

from manager.utils.tests import MultiDBTestCase


@tag(
    "program",
    "program_review_tool",
    "views",
    "program.fetch.default",
    "program_review_tool.program.fetch",
    "views.TestFetchProgram",
)
class TestFetchProgram(MultiDBTestCase):
    """
    Tests for GET /v1/program-review-tool/program endpoint.
    """

    url: str = reverse("program_review_tool.program")

    @tag("views.program.fetch_programs_by_program_ids")
    def test_fetch_programs_by_program_ids(self) -> None:
        """Success Case: Fetch all `Program` records for
        the given ids."""

    @tag("views.program.fetch_programs_by_program_ids_dne")
    def test_fetch_programs_by_program_ids_dne(self) -> None:
        """Fail Case: Fetch all `Program` records for
        ids that do not exist."""
