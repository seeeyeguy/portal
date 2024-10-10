"""
Collection of pytests for EmployeeLevel's fetch controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "directory",
    "employeelevel",
    "controllers.TestFetchEmployeeLevel",
    "directory.employeelevel.fetch",
    "employeelevel.fetch.default",
)
class TestFetchEmployeeLevel(TestCase):
    """Test suite for EmployeeLevel's fetch controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/employeelevels/employeelevels.json",
    ]

    @tag("controllers.employeelevel.fetch_employeelevels")
    def test_fetch_employee_levels(self) -> None:
        """Success Case: Fetch all `EmployeeLevel` records."""

    @tag("controllers.employeelevel.fetch_employeelevel_by_id")
    def test_fetch_employee_level_by_id(self) -> None:
        """Success Case: Fetch an `EmployeeLevel` record given an id."""

    @tag("controllers.employeelevel.fetch_employeelevel_by_id_dne")
    def test_fetch_employee_level_by_id_dne(self) -> None:
        """Fail Case: Fetch an `EmployeeLevel` record given an id where
        record does not exist."""
