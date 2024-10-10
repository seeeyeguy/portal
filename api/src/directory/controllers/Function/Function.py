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

from directory import models

LOGGER = logging.getLogger(__name__)


class Function:
    """
    Container class for functions related to retrieving `Function`
    records. `Function` helps to classify a resource within a primary
    organizational unit that encompasses a broad area of expertise
    and responsibilities within the organization.
    """

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

        optional_args = f" with id: {function_id}" if function_id else "s"
        LOGGER.info(f"Fetching Function{optional_args}.")
        # Please remove the ignore after implementation.
        return []  # type: ignore[return-value]
