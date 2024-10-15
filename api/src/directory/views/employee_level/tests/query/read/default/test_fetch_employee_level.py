"""
Collection of pytests for EmployeeLevel's fetch view endpoint.
"""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse
from rest_framework import status

from directory.controllers.EmployeeLevel.tests.query.read.default import arguments


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

        response = self.client.get(self.url)
        employee_levels = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(employee_levels, List)
        self.assertCountEqual(
            employee_levels, list(arguments.VALID_EMPLOYEELEVEL_RECORDS.values())
        )

    @tag("views.employeelevel.fetch_employeelevel_by_id")
    def test_fetch_employee_level_by_id(self) -> None:
        """Success Case: Fetch an `EmployeeLevel` record given an id."""

        request_url: str = f"{self.url}?id={arguments.FETCH_EMPLOYEELEVEL_BY_ID}"
        response = self.client.get(request_url)
        employee_level = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(employee_level, dict)
        self.assertEqual(
            employee_level,
            arguments.VALID_EMPLOYEELEVEL_RECORDS[arguments.FETCH_EMPLOYEELEVEL_BY_ID],
        )

    @tag("views.employeelevel.fetch_employeelevel_by_id_dne")
    def test_fetch_employee_level_by_id_dne(self) -> None:
        """Fail Case: Fetch an `EmployeeLevel` record given an id where
        record does not exist."""

        request_url: str = f"{self.url}?id={arguments.FETCH_EMPLOYEELEVEL_BY_ID_DNE}"
        response = self.client.get(request_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
