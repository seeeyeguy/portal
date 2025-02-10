"""
Collection of pytests for EmployeeLevel's create controller.
"""
import pytest
from typing import List

from django.test import tag, TestCase

from directory.controllers import EmployeeLevel
from directory.controllers.EmployeeLevel.tests.mutations.create.default import arguments
from directory.exceptions import DirectoryError
from directory.models.EmployeeLevel import EmployeeLevel as EmployeeLevelModel
from directory.models.EmployeeLevel.serializers import EmployeeLevelSerializer


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

        # Create `EmployeeLevel` record.
        employee_level = EmployeeLevel.create_employee_level(
            name=arguments.CREATE_EMPLOYEELEVEL_NAME_SUCCESSFUL,
            description=arguments.CREATE_EMPLOYEELEVEL_DESCRIPTION,
            level=arguments.CREATE_EMPLOYEELEVEL_LEVEL,
        )

        self.assertIsInstance(employee_level, EmployeeLevelModel)

        # Serialize `EmployeeLevel`.
        serialized_employee_level = EmployeeLevelSerializer(employee_level).data

        # Remove dynamic datetime fields before comparison.
        del serialized_employee_level["created"]
        del serialized_employee_level["modified"]

        self.assertEqual(
            serialized_employee_level, arguments.CREATE_EMPLOYEELEVEL_EXPECTED_VALUES
        )

    @tag("controllers.employeelevel.create_employee_level_duplicate_name")
    def test_create_employee_level_duplicate_name(self) -> None:
        """Fail Case: Create an `EmployeeLevel` record with a duplicate name."""

        with pytest.raises(DirectoryError):
            # Create `EmployeeLevel` record with 'name' that already exists.
            _ = EmployeeLevel.create_employee_level(
                name=arguments.CREATE_EMPLOYEELEVEL_NAME_DUPLICATE,
                description=arguments.CREATE_EMPLOYEELEVEL_DESCRIPTION,
                level=arguments.CREATE_EMPLOYEELEVEL_LEVEL,
            )

    @tag("controllers.employeelevel.create_employee_level_duplicate_level")
    def test_create_employee_level_duplicate_level(self) -> None:
        """Fail Case: Create an `EmployeeLevel` record with a duplicate level."""

        with pytest.raises(DirectoryError):
            # Create `EmployeeLevel` record with 'level' that already exists.
            _ = EmployeeLevel.create_employee_level(
                name=arguments.CREATE_EMPLOYEELEVEL_NAME_SUCCESSFUL,
                description=arguments.CREATE_EMPLOYEELEVEL_DESCRIPTION,
                level=arguments.CREATE_EMPLOYEELEVEL_LEVEL_DUPLICATE,
            )
