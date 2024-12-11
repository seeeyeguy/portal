"""
Collection of pytests for SubFunction's create view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "subfunction",
    "views",
    "directory.subfunction.create",
    "subfunction.create.default",
    "views.TestCreateSubFunction",
)
class TestCreateSubFunction(TestCase):
    """
    Tests for POST /v1/directory/subfunctions endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
    ]

    url: str = reverse("directory.subfunction")

    @tag("views.subfunction.create_subfunction")
    def test_create_subfunction(self) -> None:
        """Success Case: Create a `SubFunction` record."""

    @tag("views.subfunction.create_subfunction_duplicate_name")
    def test_create_subfunction_duplicate_name(self) -> None:
        """Fail Case: Create a `SubFunction` record with a duplicate name."""

    @tag("views.subfunction.create_subfunction_function_dne")
    def test_create_subfunction_function_dne(self) -> None:
        """Fail Case: Create a `SubFunction` record with a given
        function id where that `Function` does not exist."""
