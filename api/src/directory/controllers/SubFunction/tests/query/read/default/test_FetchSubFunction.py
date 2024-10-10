"""
Collection of pytests for SubFunction's fetch controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "directory",
    "subfunction",
    "controllers.TestFetchSubFunction",
    "directory.subfunction.fetch",
    "subfunction.fetch.default",
)
class TestFetchSubFunction(TestCase):
    """Test suite for SubFunction's fetch controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
    ]

    @tag("controllers.subfunction.fetch_subfunctions")
    def test_fetch_subfunctions(self) -> None:
        """Success Case: Fetch all `SubFunction` records."""

    @tag("controllers.subfunction.fetch_subfunction_by_id")
    def test_fetch_subfunction_by_id(self) -> None:
        """Success Case: Fetch a `SubFunction` record given an id."""

    @tag("controllers.subfunction.fetch_subfunction_by_id_dne")
    def test_fetch_subfunction_by_id_dne(self) -> None:
        """Fail Case: Fetch a `SubFunction` record given an id where
        record does not exist."""
