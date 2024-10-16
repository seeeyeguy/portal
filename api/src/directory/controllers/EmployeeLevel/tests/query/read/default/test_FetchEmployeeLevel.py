"""
Collection of pytests for EmployeeLevel's fetch controller.
"""

# pylint: disable=line-too-long,wrong-import-order
import pytest
from typing import List

from django.db.models import QuerySet
from django.test import tag, TestCase

from directory.controllers.EmployeeLevel.EmployeeLevel import EmployeeLevel
from directory.controllers.EmployeeLevel.tests.query.read.default import arguments
from directory.exceptions import DirectoryError
from directory.models.EmployeeLevel.EmployeeLevel import (
    EmployeeLevel as EmployeeLevelModel,
)
from directory.models.EmployeeLevel.serializers import EmployeeLevelSerializer


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

        employee_levels = EmployeeLevel.fetch_employee_levels()

        self.assertIsInstance(employee_levels, QuerySet[EmployeeLevelModel])
        self.assertEqual(
            employee_levels.count(), len(arguments.VALID_EMPLOYEELEVEL_RECORDS.keys())  # type: ignore[union-attr]
        )

        for employee_level in employee_levels:  # type: ignore[union-attr]
            self.assertIsInstance(employee_level, EmployeeLevelModel)

            employee_level_id: int = employee_level.id

            self.assertIn(employee_level_id, arguments.VALID_EMPLOYEELEVEL_RECORDS)
            self.assertEqual(
                EmployeeLevelSerializer(employee_level).data,
                arguments.VALID_EMPLOYEELEVEL_RECORDS[employee_level_id],
            )

    @tag("controllers.employeelevel.fetch_employeelevel_by_id")
    def test_fetch_employee_level_by_id(self) -> None:
        """Success Case: Fetch an `EmployeeLevel` record given an id."""

        employee_level = EmployeeLevel.fetch_employee_levels(
            employee_level_id=arguments.FETCH_EMPLOYEELEVEL_BY_ID
        )

        self.assertIsInstance(employee_level, EmployeeLevelModel)

        employee_level_id: int = employee_level.id  # type: ignore[union-attr]

        self.assertIn(employee_level_id, arguments.VALID_EMPLOYEELEVEL_RECORDS)
        self.assertEqual(
            EmployeeLevelSerializer(employee_level).data,
            arguments.VALID_EMPLOYEELEVEL_RECORDS[employee_level_id],
        )

    @tag("controllers.employeelevel.fetch_employeelevel_by_id_dne")
    def test_fetch_employee_level_by_id_dne(self) -> None:
        """Fail Case: Fetch an `EmployeeLevel` record given an id where
        record does not exist."""

        with pytest.raises(DirectoryError):
            _ = EmployeeLevel.fetch_employee_levels(
                employee_level_id=arguments.FETCH_EMPLOYEELEVEL_BY_ID_DNE
            )
