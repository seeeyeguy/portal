"""
`BI Portal` `EmployeeLevel` controller module. Controllers utilize
the Django ORM to fetch records within the `EmployeeLevel` table.
`EmployeeLevel` helps to classify a resource within a field of
concern in regards to a hierarchial level within the organization
such as employee, manager, or executive.
"""

import logging
from typing import Union

from django.db.models import QuerySet

from directory import models

LOGGER = logging.getLogger(__name__)


class EmployeeLevel:
    """
    Container class for functions related to retrieving `EmployeeLevel`
    records. `EmployeeLevel` helps to classify a resource within a field
    of concern in regards to a hierarchial level within the organization
    such as employee, manager, or executive.
    """

    @staticmethod
    def fetch_employee_levels(
        employee_level_id: int | None = None,
    ) -> Union[models.EmployeeLevel, QuerySet[models.EmployeeLevel]]:
        """
        Fetch an `EmployeeLevel` object from the database with the given
        id or if no id is specified return all `EmployeeLevel` objects.

        Accepts:
            * employee_level_id (int): Optional parameter to either
                return a single `EmployeeLevel` object with the specified
                id or all `EmployeeLevel` objects in the database.

        Returns:
            * employee_levels (Union[models.EmployeeLevel, QuerySet[models.EmployeeLevel]]):
                Either one `EmployeeLevel` instance with the specified id
                or a QuerySet of all `EmployeeLevel` instances.
        """

        optional_args = f" with id: {employee_level_id}" if employee_level_id else "s"
        LOGGER.info(f"Fetching EmployeeLevel{optional_args}.")
        # Please remove the ignore after implementation.
        return []  # type: ignore[return-value]
