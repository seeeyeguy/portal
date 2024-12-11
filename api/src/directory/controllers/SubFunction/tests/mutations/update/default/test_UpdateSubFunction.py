"""
Collection of pytests for SubFunction's update controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "directory",
    "subfunction",
    "controllers.TestUpdateSubFunction",
    "directory.subfunction.update",
    "subfunction.update.default",
)
class TestUpdateSubFunction(TestCase):
    """Test suite for SubFunction's update controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
    ]

    @tag("controllers.subfunction.update_subfunction")
    def test_update_subfunction(self) -> None:
        """Success Case: Update a `SubFunction` record."""

    @tag("controllers.subfunction.update_subfunction_record_dne")
    def test_update_subfunction_record_dne(self) -> None:
        """Fail Case: Update a `SubFunction` that does not exist."""

    @tag("controllers.subfunction.update_subfunction_duplicate_name")
    def test_update_subfunction_duplicate_name(self) -> None:
        """Fail Case: Update a `SubFunction` record with a duplicate name."""

    @tag("controllers.subfunction.update_subfunction_function_dne")
    def test_update_subfunction_function_dne(self) -> None:
        """Fail Case: Update a `SubFunction` record with a given
        function id where that `Function` does not exist."""
