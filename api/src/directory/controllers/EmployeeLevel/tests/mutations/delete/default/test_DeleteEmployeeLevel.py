"""
Collection of pytests for EmployeeLevel's delete controller.
"""

from typing import List

from django.test import tag, TestCase

from directory.controllers.EmployeeLevel.EmployeeLevel import EmployeeLevel
from directory.controllers.EmployeeLevel.tests.mutations.delete.default import arguments


@tag(
    "controllers",
    "directory",
    "employeelevel",
    "controllers.TestDeleteEmployeeLevel",
    "directory.employeelevel.delete",
    "employeelevel.delete.default",
)
class TestDeleteEmployeeLevel(TestCase):
    """Test suite for EmployeeLevel's delete controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/employeelevels/employeelevels.json",
    ]

    @tag("controllers.employeelevel.delete_employee_level")
    def test_delete_employee_level(self) -> None:
        """Success Case: Delete an `EmployeeLevel` record."""

        rows_affected = EmployeeLevel.delete_employee_level(
            employee_level_id=arguments.DELETE_EMPLOYEE_LEVEL_BY_ID
        )

        self.assertEqual(rows_affected, 1)
