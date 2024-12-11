"""
Collection of pytests for EmployeeLevel's delete controller.
"""

from typing import List

from django.test import tag, TestCase


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
