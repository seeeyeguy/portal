"""
Collection of pytests for EmployeeLevel's update view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "employeelevel",
    "views",
    "directory.employeelevel.update",
    "employeelevel.update.default",
    "views.TestUpdateEmployeeLevel",
)
class TestUpdateEmployeeLevel(TestCase):
    """
    Tests for PUT /v1/directory/employee-levels endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/employeelevels/employeelevels.json",
    ]

    url: str = reverse("directory.employeelevel")

    @tag("views.employeelevel.update_employee_level")
    def test_update_employee_level(self) -> None:
        """Success Case: Update an `EmployeeLevel` record."""

    @tag("views.employeelevel.update_employee_level_record_dne")
    def test_update_employee_level_record_dne(self) -> None:
        """Fail Case: Update an `EmployeeLevel` that does not exist."""

    @tag("views.employeelevel.update_employee_level_duplicate_name")
    def test_update_employee_level_duplicate_name(self) -> None:
        """Fail Case: Update an `EmployeeLevel` record with a duplicate name."""
