"""
Collection of pytests for EmployeeLevel's update view endpoint.
"""

from typing import List

from django.contrib.auth.models import User
from django.test import tag
from django.urls import reverse
from rest_framework import status

from directory.controllers.EmployeeLevel.tests.mutations.update.default import arguments

from manager.utils.tests import MultiDBTestCase


@tag(
    "directory",
    "employeelevel",
    "views",
    "directory.employeelevel.update",
    "employeelevel.update.default",
    "views.TestUpdateEmployeeLevel",
)
class TestUpdateEmployeeLevel(MultiDBTestCase):
    """
    Tests for PUT /v1/directory/employee-levels endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = User.objects.get(email__iexact=arguments.UPDATE_EMPLOYEELEVEL_USER_EMAIL)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        "portal/models/fixtures/employeelevels/employeelevels.json",
        "portal/models/fixtures/users/users.json",
    ]

    url: str = reverse("directory.employeelevel")

    @tag("views.employeelevel.update_employee_level")
    def test_update_employee_level(self) -> None:
        """Success Case: Update an `EmployeeLevel` record."""

        body: dict = {
            "name": arguments.UPDATE_EMPLOYEELEVEL_NAME,
            "description": arguments.UPDATE_EMPLOYEELEVEL_DESCRIPTION,
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_EMPLOYEELEVEL_ID}"

        # Make request to update `EmployeeLevel`.
        response = self.client.put(request_url, body, content_type="application/json")

        employee_level = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(employee_level, dict)

        # Remove dynamic datetime fields before comparison.
        del employee_level["created"]
        del employee_level["modified"]

        self.assertEqual(employee_level, arguments.UPDATE_EMPLOYEELEVEL_EXPECTED_VALUES)

    @tag("views.employeelevel.update_employee_level_record_dne")
    def test_update_employee_level_record_dne(self) -> None:
        """Fail Case: Update an `EmployeeLevel` that does not exist."""

        body: dict = {
            "name": arguments.UPDATE_EMPLOYEELEVEL_NAME_DNE,
            "description": arguments.UPDATE_EMPLOYEELEVEL_DESCRIPTION,
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_EMPLOYEELEVEL_DNE}"

        # Make request to update `EmployeeLevel`.
        response = self.client.put(request_url, body, content_type="application/json")
        # Ensure the response status code is 404.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.employeelevel.update_employee_level_duplicate_name")
    def test_update_employee_level_duplicate_name(self) -> None:
        """Fail Case: Update an `EmployeeLevel` record with a duplicate name."""

        body: dict = {
            "name": arguments.UPDATE_EMPLOYEELEVEL_DUPLICATE_NAME,
            "description": arguments.UPDATE_EMPLOYEELEVEL_DESCRIPTION,
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_EMPLOYEELEVEL_ID}"

        # Make request to update `EmployeeLevel`.
        response = self.client.put(request_url, body, content_type="application/json")
        # Ensure the response status code is 400.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
