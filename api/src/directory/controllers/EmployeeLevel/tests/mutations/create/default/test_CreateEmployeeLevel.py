"""
Collection of pytests for EmployeeLevel's create controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "directory",
    "employeelevel",
    "controllers.TestCreateEmployeeLevel",
    "directory.employeelevel.create",
    "employeelevel.create.default",
)
class TestCreateEmployeeLevel(TestCase):
    """Test suite for EmployeeLevel's create controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/employeelevels/employeelevels.json",
    ]

    @tag("controllers.employeelevel.create_employee_level")
    def test_create_employee_level(self) -> None:
        """Success Case: Create an `EmployeeLevel` record."""

    @tag("controllers.employeelevel.create_employee_level_duplicate_name")
    def test_create_employee_level_duplicate_name(self) -> None:
        """Fail Case: Create an `EmployeeLevel` record with a duplicate name."""
