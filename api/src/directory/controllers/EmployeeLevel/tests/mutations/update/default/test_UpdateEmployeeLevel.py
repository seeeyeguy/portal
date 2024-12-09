"""
Collection of pytests for EmployeeLevel's update controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "directory",
    "employeelevel",
    "controllers.TestUpdateEmployeeLevel",
    "directory.employeelevel.update",
    "employeelevel.update.default",
)
class TestUpdateEmployeeLevel(TestCase):
    """Test suite for EmployeeLevel's update controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/employeelevels/employeelevels.json",
    ]

    @tag("controllers.employeelevel.update_employee_level")
    def test_create_employee_level(self) -> None:
        """Success Case: Update an `EmployeeLevel` record."""

    @tag("controllers.employeelevel.update_employee_level_record_dne")
    def test_create_employee_level_record_dne(self) -> None:
        """Fail Case: Update an `EmployeeLevel` that does not exist."""

    @tag("controllers.employeelevel.update_employee_level_duplicate_name")
    def test_update_employee_level_duplicate_name(self) -> None:
        """Fail Case: Update an `EmployeeLevel` record with a duplicate name."""
