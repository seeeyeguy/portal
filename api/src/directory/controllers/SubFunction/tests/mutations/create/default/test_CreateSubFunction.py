"""
Collection of pytests for SubFunction's create controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "directory",
    "subfunction",
    "controllers.TestCreateSubFunction",
    "directory.subfunction.create",
    "subfunction.create.default",
)
class TestCreateSubFunction(TestCase):
    """Test suite for SubFunction's create controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
    ]

    @tag("controllers.subfunction.create_subfunction")
    def test_create_subfunction(self) -> None:
        """Success Case: Create a `SubFunction` record."""

    @tag("controllers.subfunction.create_subfunction_duplicate_name")
    def test_create_subfunction_duplicate_name(self) -> None:
        """Fail Case: Create a `SubFunction` record with a duplicate name."""

    @tag("controllers.subfunction.create_subfunction_function_dne")
    def test_create_subfunction_function_dne(self) -> None:
        """Fail Case: Create a `SubFunction` record with a given
        function id where that `Function` does not exist."""
