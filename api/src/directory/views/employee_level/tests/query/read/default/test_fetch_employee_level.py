"""
Collection of pytests for EmployeeLevel's fetch view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "directory",
    "employeelevel",
    "views",
    "directory.employeelevel.fetch",
    "employeelevel.fetch.default",
    "views.TestFetchEmployeeLevel",
)
class TestFetchEmployeeLevel(TestCase):
    """
    Tests for GET /v1/directory/employee-levels endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/employeelevels/employeelevels.json",
    ]

    url: str = reverse("directory.employeelevel")

    @tag("views.employeelevel.fetch_employeelevels")
    def test_fetch_employee_levels(self) -> None:
        """Success Case: Fetch all `EmployeeLevel` records."""

    @tag("views.employeelevel.fetch_employeelevel_by_id")
    def test_fetch_employee_level_by_id(self) -> None:
        """Success Case: Fetch an `EmployeeLevel` record given an id."""

    @tag("views.employeelevel.fetch_employeelevel_by_id_dne")
    def test_fetch_employee_level_by_id_dne(self) -> None:
        """Fail Case: Fetch an `EmployeeLevel` record given an id where
        record does not exist."""
