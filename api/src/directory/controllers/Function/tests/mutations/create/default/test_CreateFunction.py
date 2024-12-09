"""
Collection of pytests for Function's create controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "directory",
    "function",
    "controllers.TestCreateFunction",
    "directory.function.create",
    "function.create.default",
)
class TestCreateFunction(TestCase):
    """Test suite for Function's create controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
    ]

    @tag("controllers.function.create_function")
    def test_create_function(self) -> None:
        """Success Case: Create a `Function` record."""

    @tag("controllers.function.create_function_duplicate_name")
    def test_create_function_duplicate_name(self) -> None:
        """Fail Case: Create a `Function` record with a duplicate name."""
