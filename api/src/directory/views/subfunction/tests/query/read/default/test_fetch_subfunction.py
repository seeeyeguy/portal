"""
Collection of pytests for SubFunction's fetch view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "subfunction",
    "views",
    "directory.subfunction.fetch",
    "subfunction.fetch.default",
    "views.TestFetchSubFunction",
)
class TestFetchSubFunction(TestCase):
    """
    Tests for GET /v1/directory/subfunctions endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
    ]

    url: str = reverse("directory.subfunction")

    @tag("views.subfunction.fetch_subfunctions")
    def test_fetch_subfunctions(self) -> None:
        """Success Case: Fetch all `SubFunction` records."""

    @tag("views.subfunction.fetch_subfunction_by_id")
    def test_fetch_subfunction_by_id(self) -> None:
        """Success Case: Fetch a `SubFunction` record given an id."""

    @tag("views.subfunction.fetch_subfunction_by_id_dne")
    def test_fetch_subfunction_by_id_dne(self) -> None:
        """Fail Case: Fetch a `SubFunction` record given an id where
        record does not exist."""
