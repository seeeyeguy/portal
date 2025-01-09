"""
`BI Portal` `EmployeeLevel` controller module. Controllers utilize
the Django ORM to fetch records within the `EmployeeLevel` table.
`EmployeeLevel` helps to classify a resource within a field of
concern in regards to a hierarchial level within the organization
such as employee, manager, or executive.
"""

import logging
from typing import Union

from django.db import transaction
from django.db.models import QuerySet
from django.db.utils import IntegrityError

from directory import exceptions, models

LOGGER = logging.getLogger(__name__)


class EmployeeLevel:
    """
    Container class for functions related to creating, updating, deleting,
    and retrieving `EmployeeLevel` records. `EmployeeLevel` helps to
    classify a resource within a field of concern in regards to a hierarchial
    level within the organization such as employee, manager, or executive.
    """

    @staticmethod
    def create_employee_level(name: str, description: str) -> models.EmployeeLevel:
        """
        Create an `EmployeeLevel` record with the given name and description.

        Accepts:
            * name (str): The name of the `EmployeeLevel`.
            * description (str): A short/detailed description of what
                this `EmployeeLevel` is.

        Returns:
            * employee_level (models.EmployeeLevel): The `EmployeeLevel`
                record created.
        """

        LOGGER.info(
            f"Creating EmployeeLevel with name: {name} and description: {description}."
        )
        # Please remove the ignore after implementation.
        return {}  # type: ignore[return-value]

    @staticmethod
    def update_employee_level(
        employee_level_id: int, name: str, description: str
    ) -> models.EmployeeLevel:
        """
        Update an `EmployeeLevel` record for the given id with the
        given name and description.

        Accepts:
            * employee_level_id (int): The id of the record being updated.
            * name (str): The name of the `EmployeeLevel`.
            * description (str): A short/detailed description of what
                this `EmployeeLevel` is.

        Returns:
            * employee_level (models.EmployeeLevel): The `EmployeeLevel`
                record updated.
        """

        try:
            LOGGER.info(
                f"Updating EmployeeLevel with id: {employee_level_id} "
                f"with name: {name} and description: {description}."
            )

            # Query `EmployeeLevel` for the instance id given.
            employee_level_record: models.EmployeeLevel = (
                models.EmployeeLevel.objects.get(id=employee_level_id)
            )

            # If there's no field to update, do not hit the database and
            # return existing record.
            if (
                employee_level_record.name == name
                and employee_level_record.description == description
            ):
                return employee_level_record

            # Update `EmployeeLevel` record with the given name and description.
            employee_level_record.name = name
            employee_level_record.description = description
            employee_level_record.save()

            return employee_level_record
        except models.EmployeeLevel.DoesNotExist as exc:
            err_msg: str = f"EmployeeLevel (id={employee_level_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, 404) from exc
        except IntegrityError as exc:
            err_msg: str = "Invalid parameters given."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, 400) from exc

    @staticmethod
    def delete_employee_level(employee_level_id: int) -> int:
        """
        Delete the `EmployeeLevel` record with the given id.

        Accepts:
            * employee_level_id (int): The id of the record to be deleted.

        Returns:
            * rows_affected (int): The number of rows removed.
        """

        try:
            LOGGER.info(f"Deleting EmployeeLevel with id: {employee_level_id}.")

            # Delete the corresponding `EmployeeLevel` record.
            employee_level_record: models.EmployeeLevel = models.EmployeeLevel.objects.get(id=employee_level_id)

            rows_affected, _ = employee_level_record.delete()

            return rows_affected

        except models.EmployeeLevel.DoesNotExist as exc:
            err_msg = f"Employee Level (id={employee_level_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, 404) from exc

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
            * employee_levels (
                    Union[
                        models.EmployeeLevel,
                        QuerySet[models.EmployeeLevel]
                    ]
                ):
                Either one `EmployeeLevel` instance with the specified id
                or a QuerySet of all `EmployeeLevel` instances.
        """

        try:
            optional_args = (
                f" with id: {employee_level_id}" if employee_level_id else "s"
            )
            LOGGER.info(f"Fetching EmployeeLevel{optional_args}.")

            # If an employee level id is given, fetch the corresponding
            # `EmployeeLevel` record, else all `EmployeeLevel` records.
            employee_levels: Union[
                models.EmployeeLevel, QuerySet[models.EmployeeLevel]
            ] = (
                models.EmployeeLevel.objects.get(id=employee_level_id)
                if employee_level_id
                else models.EmployeeLevel.objects.all()
            )
            return employee_levels
        except models.EmployeeLevel.DoesNotExist as exc:
            err_msg = f"Employee Level (id={employee_level_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, 404) from exc
