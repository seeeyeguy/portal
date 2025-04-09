"""
Collection of pytests for Program's review controller.
"""

# pylint: disable=line-too-long,wrong-import-order
from django.test import tag

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

    @tag("controllers.program.review_programs_by_program_ids")
    def test_fetch_programs_by_program_ids(self) -> None:
        """Success Case: Review `Program` records for
        the given ids."""

    @tag("controllers.program.review_programs_by_program_ids_dne")
    def test_review_programs_by_program_ids_dne(self) -> None:
        """Fail Case: Review `Program` records for
        ids that do not exist."""
