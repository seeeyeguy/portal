"""
Collection of pytests for EmployeeLevel's delete view endpoint.
"""

from typing import List

from django.contrib.auth.models import User
from django.test import tag, TestCase
from django.urls import reverse
from rest_framework import status

from directory.controllers.EmployeeLevel.tests.mutations.delete.default import arguments


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

    def setUp(self) -> None:
        super().setUp()
        user = User.objects.get(email=arguments.DELETE_EMPLOYEE_LEVEL_USER_EMAIL)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        "portal/models/fixtures/employeelevels/employeelevels.json",
        "portal/models/fixtures/users/users.json",
    ]

    url: str = reverse("directory.employeelevel")

    @tag("views.employeelevel.delete_employee_level")
    def test_delete_employee_level(self) -> None:
        """Success Case: Delete an `EmployeeLevel` record."""

        request_url: str = f"{self.url}?id={arguments.DELETE_EMPLOYEE_LEVEL_BY_ID}"
        response = self.client.delete(request_url)

        rows_affected = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(rows_affected, 1)
