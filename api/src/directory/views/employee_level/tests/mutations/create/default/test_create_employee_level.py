"""
Collection of pytests for EmployeeLevel's create view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "employeelevel",
    "views",
    "directory.employeelevel.create",
    "employeelevel.create.default",
    "views.TestCreateEmployeeLevel",
)
class TestCreateEmployeeLevel(TestCase):
    """
    Tests for POST /v1/directory/employee-levels endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/employeelevels/employeelevels.json",
    ]

    url: str = reverse("directory.employeelevel")

    @tag("views.employeelevel.create_employee_level")
    def test_create_employee_level(self) -> None:
        """Success Case: Create an `EmployeeLevel` record."""

    @tag("views.employeelevel.create_employee_level_duplicate_name")
    def test_create_employee_level_duplicate_name(self) -> None:
        """Fail Case: Create an `EmployeeLevel` record with a duplicate name."""
