"""
Collection of pytests for Function's update controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "directory",
    "function",
    "controllers.TestUpdateFunction",
    "directory.function.update",
    "function.update.default",
)
class TestUpdateFunction(TestCase):
    """Test suite for Function's update controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
    ]

    @tag("controllers.function.update_function")
    def test_update_function(self) -> None:
        """Success Case: Update a `Function` record."""

    @tag("controllers.function.update_function_record_dne")
    def test_update_function_record_dne(self) -> None:
        """Fail Case: Update a `Function` that does not exist."""

    @tag("controllers.function.update_function_duplicate_name")
    def test_update_function_duplicate_name(self) -> None:
        """Fail Case: Update a `Function` record with a duplicate name."""
