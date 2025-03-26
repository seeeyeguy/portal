"""
Collection of pytests for Function's delete controller.
"""

from typing import List

from django.test import tag

from directory.controllers.Function.Function import Function
from directory.controllers.Function.tests.mutations.delete.default import arguments

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "directory",
    "function",
    "controllers.TestDeleteFunction",
    "directory.function.delete",
    "function.delete.default",
)
class TestDeleteFunction(MultiDBTestCase):
    """Test suite for Function's delete controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
    ]

    @tag("controllers.function.delete_function")
    def test_delete_function(self) -> None:
        """Success Case: Delete a `Function` record."""

        rows_affected = Function.delete_function(
            function_id=arguments.DELETE_FUNCTION_BY_ID
        )
        self.assertEqual(rows_affected, 1)
