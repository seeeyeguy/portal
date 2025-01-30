"""
`BI Portal` `SubFunction` controller module. Controllers utilize the
Django ORM to fetch records within the `SubFunction` table. `SubFunction`
helps to classify a resource within a specialized division within a
`Function` that focuses on a more specific area of expertise.
"""

import logging
from typing import Tuple, Union

from django.db.models import QuerySet

from directory.models import Function
from directory import exceptions, models

LOGGER = logging.getLogger(__name__)


class SubFunction:
    """
    Container class for functions related to creating, updating,
    deleting, and retrieving `SubFunction` records. `SubFunction`
    helps to classify a resource within a specialized division
    within a `Function` that focuses on a more specific area of
    expertise.
    """

    @staticmethod
    def create_subfunction(
        name: str, description: str, function: int
    ) -> models.SubFunction:
        """
        Create a `SubFunction` record with the given name, description,
        and `Function`.

        Accepts:
            * name (str): The name of the `SubFunction`.
            * description (str): A short/detailed description of what
                this `SubFunction` is.
            * function (int): The id of the `Function` that this `SubFunction`
                relates to.

        Returns:
            * subfunction (models.SubFunction): The `SubFunction` record created.
        """

        try:
            LOGGER.info(
                f"Creating SubFunction with name: {name}, description: {description}, "
                f"and Function id: {function}."
            )

            subfunction_query: QuerySet[
                models.SubFunction
            ] = models.SubFunction.objects.filter(name__iexact=name)

            if subfunction_query.exists():
                err_msg = f"SubFunction (name={name}) already exists."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, 400)

            # Fetch `Function` record.
            function_record: Function = Function.objects.get(id=function)

            subfunction: models.SubFunction = models.SubFunction.objects.create(
                name=name.title(),
                description=description,
                function=function_record,
            )

            return subfunction
        except Function.DoesNotExist as exc:
            err_msg = f"The Function (id={function}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, 404) from exc

    @staticmethod
    def update_subfunction(
        subfunction_id: int, name: str, description: str, function: int
    ) -> Tuple[models.SubFunction, int]:
        """
        Update a `SubFunction` record for the given id with the given
        name, description, and `Function`.

        Accepts:
            * subfunction_id (int): The id of the record to be updated.
            * name (str): The name of the `SubFunction`.
            * description (str): A short/detailed description of what
                this `SubFunction` is.
            * function (int): The id of the `Function` that this `SubFunction`
                relates to.

        Returns:
            * subfunction (models.SubFunction): The updated `SubFunction` record.
            * rows_affected (int): The number of `SubFunction` records updated.
        """

        try:
            LOGGER.info(
                f"Updating SubFunction with id: {subfunction_id} with name: {name}, "
                f"description: {description}, and Function id: {function}."
            )

            # Fetch `Function` record by id.
            function_record: models.Function = models.Function.objects.get(id=function)

            # Fetch `SubFunction` record by id.
            subfunction: models.SubFunction = models.SubFunction.objects.get(
                id=subfunction_id
            )

            # Check for existing `SubFunction` with given name, excluding
            # the target `SubFunction`.
            if (
                models.SubFunction.objects.filter(name=name)
                .exclude(id=subfunction_id)
                .exists()
            ):
                err_msg = f"SubFunction with name: {name} already exists."
                LOGGER.error(err_msg)
                raise exceptions.DirectoryError(err_msg, 400)

            # Update the `SubFunction` record.
            rows_affected: int = models.SubFunction.objects.filter(
                id=subfunction_id
            ).update(name=name, description=description, function=function_record)

            subfunction.refresh_from_db()

            return subfunction, rows_affected
        except models.Function.DoesNotExist as exc:
            err_msg = f"Function (id={function}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, 404) from exc
        except models.SubFunction.DoesNotExist as exc:
            err_msg = f"SubFunction (id={subfunction_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, 404) from exc

    @staticmethod
    def delete_subfunction(subfunction_id: int) -> int:
        """
        Delete the `SubFunction` record with the given id.

        Accepts:
            * subfunction_id (int): The id of the record to be deleted.

        Returns:
            * rows_affected (int): The number of rows removed.
        """

        LOGGER.info(f"Deleting SubFunction with id: {subfunction_id}.")

        # Delete `SubFunction` record.
        rows_affected, _ = models.SubFunction.objects.filter(id=subfunction_id).delete()

        return rows_affected

    @staticmethod
    def fetch_subfunctions(
        subfunction_id: int | None = None,
    ) -> Union[models.SubFunction, QuerySet[models.SubFunction]]:
        """
        Fetch a `SubFunction` object from the database with the given
        id or if no id is specified return all `SubFunction` objects.

        Accepts:
            * subfunction_id (int): Optional parameter to either
                return a single `SubFunction` object with the specified
                id or all `SubFunction` objects in the database.

        Returns:
            * subfunctions (Union[models.SubFunction, QuerySet[models.SubFunction]]):
                Either one `SubFunction` instance with the specified id
                or a QuerySet of all `SubFunction` instances.
        """

        try:
            optional_args = f" with id: {subfunction_id}" if subfunction_id else "s"
            LOGGER.info(f"Fetching SubFunction{optional_args}.")

            # If a subfunction id is given, fetch the corresponding
            # `SubFunction` record, else all `SubFunction` records.
            subfunctions: Union[models.SubFunction, QuerySet[models.SubFunction]] = (
                models.SubFunction.objects.get(id=subfunction_id)
                if subfunction_id
                else models.SubFunction.objects.all()
            )
            return subfunctions
        except models.SubFunction.DoesNotExist as exc:
            err_msg = f"SubFunction (id={subfunction_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, 404) from exc
