"""
Collection of pytests for EmployeeLevel's update controller.
"""

import pytest
from typing import List

from django.test import tag, TestCase

from directory.controllers import EmployeeLevel
from directory.controllers.EmployeeLevel.tests.mutations.update.default import arguments
from directory.exceptions import DirectoryError
from directory.models.EmployeeLevel import EmployeeLevel as EmployeeLevelModel
from directory.models.EmployeeLevel.serializers import EmployeeLevelSerializer


@tag(
    "controllers",
    "directory",
    "employeelevel",
    "controllers.TestUpdateEmployeeLevel",
    "directory.employeelevel.update",
    "employeelevel.update.default",
)
class TestUpdateEmployeeLevel(TestCase):
    """Test suite for EmployeeLevel's update controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/employeelevels/employeelevels.json",
    ]

    @tag("controllers.employeelevel.update_employee_level")
    def test_create_employee_level(self) -> None:
        """Success Case: Update an `EmployeeLevel` record."""

        # Update `EmployeeLevel` record.
        employee_level_record = EmployeeLevel.update_employee_level(
            employee_level_id=arguments.UPDATE_EMPLOYEELEVEL_ID,
            name=arguments.UPDATE_EMPLOYEELEVEL_NAME,
            description=arguments.UPDATE_EMPLOYEELEVEL_DESCRIPTION,
        )

        self.assertIsInstance(employee_level_record, EmployeeLevelModel)

        # Serialize `EmployeeLevel`.
        serialized_employee_level = EmployeeLevelSerializer(employee_level_record).data

        # Remove dynamic datetime fields before comparison.
        del serialized_employee_level["created"]
        del serialized_employee_level["modified"]

        self.assertEqual(
            serialized_employee_level, arguments.UPDATE_EMPLOYEELEVEL_EXPECTED_VALUES
        )

    @tag("controllers.employeelevel.update_employee_level_record_dne")
    def test_create_employee_level_record_dne(self) -> None:
        """Fail Case: Update an `EmployeeLevel` that does not exist."""

        with pytest.raises(DirectoryError):
            _ = EmployeeLevel.update_employee_level(
                employee_level_id=arguments.UPDATE_EMPLOYEELEVEL_DNE,
                name=arguments.UPDATE_EMPLOYEELEVEL_NAME,
                description=arguments.UPDATE_EMPLOYEELEVEL_DESCRIPTION,
            )

    @tag("controllers.employeelevel.update_employee_level_duplicate_name")
    def test_update_employee_level_duplicate_name(self) -> None:
        """Fail Case: Update an `EmployeeLevel` record with a duplicate name."""

        with pytest.raises(DirectoryError):
            _ = EmployeeLevel.update_employee_level(
                employee_level_id=arguments.UPDATE_EMPLOYEELEVEL_ID,
                name=arguments.UPDATE_EMPLOYEELEVEL_DUPLICATE_NAME,
                description=arguments.UPDATE_EMPLOYEELEVEL_DESCRIPTION,
            )
