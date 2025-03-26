"""
Collection of pytests for SubFunction's delete controller.
"""

from typing import List

from django.test import tag

from directory.controllers.SubFunction.SubFunction import SubFunction
from directory.controllers.SubFunction.tests.mutations.delete.default import arguments

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "directory",
    "subfunction",
    "controllers.TestDeleteSubFunction",
    "directory.subfunction.delete",
    "subfunction.delete.default",
)
class TestDeleteSubFunction(MultiDBTestCase):
    """Test suite for SubFunction's delete controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
    ]

    @tag("controllers.subfunction.delete_subfunction")
    def test_delete_subfunction(self) -> None:
        """Success Case: Delete a `SubFunction` record."""

        rows_affected = SubFunction.delete_subfunction(
            subfunction_id=arguments.DELETE_SUBFUNCTION_SUBFUNCTION_ID
        )

        self.assertEqual(rows_affected, arguments.DELETE_SUBFUNCTION_ROWS_AFFECTED)
