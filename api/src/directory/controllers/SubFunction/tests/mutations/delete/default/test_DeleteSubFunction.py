"""
Collection of pytests for SubFunction's delete controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "directory",
    "subfunction",
    "controllers.TestDeleteSubFunction",
    "directory.subfunction.delete",
    "subfunction.delete.default",
)
class TestDeleteSubFunction(TestCase):
    """Test suite for SubFunction's delete controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
    ]

    @tag("controllers.subfunction.delete_subfunction")
    def test_delete_subfunction(self) -> None:
        """Success Case: Delete a `SubFunction` record."""
