"""
Collection of pytests for SubFunction's update view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "subfunction",
    "views",
    "directory.subfunction.update",
    "subfunction.update.default",
    "views.TestUpdateSubFunction",
)
class TestUpdateSubFunction(TestCase):
    """
    Tests for PUT /v1/directory/subfunctions endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
    ]

    url: str = reverse("directory.subfunction")

    @tag("views.subfunction.update_subfunction")
    def test_update_subfunction(self) -> None:
        """Success Case: Update a `SubFunction` record."""

    @tag("views.subfunction.update_subfunction_record_dne")
    def test_update_subfunction_record_dne(self) -> None:
        """Fail Case: Update a `SubFunction` that does not exist."""

    @tag("views.subfunction.update_subfunction_duplicate_name")
    def test_update_subfunction_duplicate_name(self) -> None:
        """Fail Case: Update a `SubFunction` record with a duplicate name."""

    @tag("views.subfunction.update_subfunction_function_dne")
    def test_update_subfunction_function_dne(self) -> None:
        """Fail Case: Update a `SubFunction` record with a given
        function id where that `Function` does not exist."""
