"""
`BI Portal` `SubFunction` controller module. Controllers utilize the
Django ORM to fetch records within the `SubFunction` table. `SubFunction`
helps to classify a resource within a specialized division within a
`Function` that focuses on a more specific area of expertise.
"""

import logging
from typing import Union

from django.db.models import QuerySet

from directory import exceptions, models

LOGGER = logging.getLogger(__name__)


class SubFunction:
    """
    Container class for functions related to retrieving `SubFunction`
    records. `SubFunction` helps to classify a resource within a
    specialized division within a `Function` that focuses on a more
    specific area of expertise.
    """

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
