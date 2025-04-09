"""
Collection of pytests for Program's fetch controller.
"""

# pylint: disable=line-too-long,wrong-import-order
from django.test import tag

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "program",
    "program_review_tool",
    "controllers.TestFetchProgram",
    "program.fetch.default",
    "program_review_tool.program.fetch",
)
class TestFetchProgram(MultiDBTestCase):
    """Test suite for Program's fetch controller."""

    @tag("controllers.program.fetch_programs_by_program_ids")
    def test_fetch_programs_by_program_ids(self) -> None:
        """Success Case: Fetch all `Program` records for
        the given ids."""

    @tag("controllers.program.fetch_programs_by_program_ids_dne")
    def test_fetch_programs_by_program_ids_dne(self) -> None:
        """Fail Case: Fetch all `Program` records for
        ids that do not exist."""
