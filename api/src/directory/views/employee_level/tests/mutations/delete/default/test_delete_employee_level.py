"""
Collection of pytests for EmployeeLevel's delete view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "employeelevel",
    "views",
    "directory.employeelevel.delete",
    "employeelevel.delete.default",
    "views.TestDeleteEmployeeLevel",
)
class TestDeleteEmployeeLevel(TestCase):
    """
    Tests for DELETE /v1/directory/employee-levels endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/employeelevels/employeelevels.json",
    ]

    url: str = reverse("directory.employeelevel")

    @tag("views.employeelevel.delete_employee_level")
    def test_delete_employee_level(self) -> None:
        """Success Case: Delete an `EmployeeLevel` record."""
