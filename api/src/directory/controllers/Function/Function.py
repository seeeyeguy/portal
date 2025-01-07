"""
`BI Portal` `Function` controller module. Controllers utilize the
Django ORM to fetch records within the `Function` table. `Function`
helps to classify a resource within a primary organizational unit
that encompasses a broad area of expertise and responsibilities
within the organization.
"""

import logging
from typing import Union

from django.db.models import QuerySet

from directory import exceptions, models

LOGGER = logging.getLogger(__name__)


class Function:
    """
    Container class for functions related to creating, updating, deleting,
    and retrieving `Function` records. `Function` helps to classify a
    resource within a primary organizational unit that encompasses a broad
    area of expertise and responsibilities within the organization.
    """

    @staticmethod
    def create_function(name: str, description: str) -> models.Function:
        """
        Create a `Function` record with the given name and description.

        Accepts:
            * name (str): The name of the `Function`.
            * description (str): A short/detailed description of what
                this `Function` is.

        Returns:
            * function (models.Function): The `Function` record created.
        """

        LOGGER.info(
            f"Creating Function with name: {name} and description: {description}."
        )
        # Please remove the ignore after implementation.
        return {}  # type: ignore[return-value]

    @staticmethod
    def update_function(
        function_id: int, name: str, description: str
    ) -> models.Function:
        """
        Update a `Function` record for the given id with the given
        name and description.

        Accepts:
            * function_id (int): The id of the record to be updated.
            * name (str): The name of the `Function`.
            * description (str): A short/detailed description of what
                this `Function` is.

        Returns:
            * function (models.Function): The `Function` record updated.
        """

        LOGGER.info(
            f"Updating Function with id: {function_id} with name: {name} "
            f"and description: {description}."
        )
        # Please remove the ignore after implementation.
        return {}  # type: ignore[return-value]

    @staticmethod
    def delete_function(function_id: int) -> int:
        """
        Delete the `Function` record with the given id.

        Accepts:
            * function_id (int): The id of the record to be deleted.

        Returns:
            * rows_affected (int): The number of rows removed.
        """

        try:
            LOGGER.info(f"Deleting Function with id: {function_id}.")

            # Fetch the corresponding `Function` record.
            function_record: models.Function = models.Function.objects.get(
                id=function_id
            )

            # Delete `Function` record.
            rows_affected, _ = function_record.delete()

            return rows_affected
        except models.Function.DoesNotExist as exc:
            err_msg = f"Function (id={function_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, 404) from exc

    @staticmethod
    def fetch_functions(
        function_id: int | None = None,
    ) -> Union[models.Function, QuerySet[models.Function]]:
        """
        Fetch a `Function` object from the database with the given
        id or if no id is specified return all `Function` objects.

        Accepts:
            * function_id (int): Optional parameter to either
                return a single `Function` object with the specified
                id or all `Function` objects in the database.

        Returns:
            * functions (Union[models.Function, QuerySet[models.Function]]):
                Either one `Function` instance with the specified id
                or a QuerySet of all `Function` instances.
        """

        try:

            optional_args = f" with id: {function_id}" if function_id else "s"
            LOGGER.info(f"Fetching Function{optional_args}.")

            # If a function id is given, fetch the corresponding `Function` record,
            # else all `Function` records.
            functions: Union[models.Function, QuerySet[models.Function]] = (
                models.Function.objects.get(id=function_id)
                if function_id
                else models.Function.objects.all()
            )

            return functions
        except models.Function.DoesNotExist as exc:
            err_msg = f"Function (id={function_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, 404) from exc
