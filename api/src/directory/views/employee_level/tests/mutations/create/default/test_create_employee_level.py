"""
Collection of pytests for EmployeeLevel's create view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from directory.controllers.EmployeeLevel.tests.mutations.create.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "directory",
    "employeelevel",
    "views",
    "directory.employeelevel.create",
    "employeelevel.create.default",
    "views.TestCreateEmployeeLevel",
)
class TestCreateEmployeeLevel(MultiDBTestCase):
    """
    Tests for POST /v1/directory/employee-levels endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(
            email=arguments.CREATE_EMPLOYEELEVEL_USER_EMAIL_SUPERUSER
        )
        self.client.force_login(user=user)

    fixtures: List[str] = [*COMMON_FIXTURES]

    url: str = reverse("directory.employeelevel")

    @tag("views.employeelevel.create_employee_level")
    def test_create_employee_level(self) -> None:
        """Success Case: Create an `EmployeeLevel` record."""

        body: dict = {
            "name": arguments.CREATE_EMPLOYEELEVEL_NAME,
            "description": arguments.CREATE_EMPLOYEELEVEL_DESCRIPTION,
            "level": arguments.CREATE_EMPLOYEELEVEL_LEVEL,
        }

        # Make request to create `EmployeeLevel`.
        response = self.client.post(self.url, body, content_type="application/json")

        employee_level = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(employee_level, dict)

        # Remove dynamic datetime fields before comparison.
        del employee_level["created"]
        del employee_level["modified"]

        self.assertEqual(employee_level, arguments.CREATE_EMPLOYEELEVEL_EXPECTED_VALUES)

    @tag("views.employeelevel.create_employee_level_duplicate_name")
    def test_create_employee_level_duplicate_name(self) -> None:
        """Fail Case: Create an `EmployeeLevel` record with a duplicate name."""

        body: dict = {
            "name": arguments.CREATE_EMPLOYEELEVEL_NAME_DUPLICATE,
            "description": arguments.CREATE_EMPLOYEELEVEL_DESCRIPTION,
            "level": arguments.CREATE_EMPLOYEELEVEL_LEVEL,
        }

        # Make request to create `EmployeeLevel`.
        response = self.client.post(self.url, body, content_type="application/json")

        employee_level = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.employeelevel.create_employee_level_duplicate_level")
    def test_create_employee_level_duplicate_level(self) -> None:
        """Fail Case: Create an `EmployeeLevel` record with a duplicate level."""

        body: dict = {
            "name": arguments.CREATE_EMPLOYEELEVEL_NAME,
            "description": arguments.CREATE_EMPLOYEELEVEL_DESCRIPTION,
            "level": arguments.CREATE_EMPLOYEELEVEL_LEVEL_DUPLICATE,
        }

        # Make request to create `EmployeeLevel`.
        response = self.client.post(self.url, body, content_type="application/json")

        employee_level = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.employeelevel.create_employee_level_nonsuperuser")
    def test_create_employee_level_nonsuperuser(self) -> None:
        """Fail Case: Create an `EmployeeLevel` when 'is_superuser' is False."""

        user = AuthModels.User.objects.get(
            email=arguments.CREATE_EMPLOYEELEVEL_USER_EMAIL_NONSUPERUSER
        )
        self.client.force_login(user=user)

        body: dict = {
            "name": arguments.CREATE_EMPLOYEELEVEL_NAME,
            "description": arguments.CREATE_EMPLOYEELEVEL_DESCRIPTION,
            "level": arguments.CREATE_EMPLOYEELEVEL_LEVEL,
        }

        # Make request to create `EmployeeLevel`.
        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
