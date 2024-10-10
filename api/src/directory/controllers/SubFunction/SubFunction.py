"""
`BI Portal` `SubFunction` controller module. Controllers utilize the
Django ORM to fetch records within the `SubFunction` table. `SubFunction`
helps to classify a resource within a specialized division within a
`Function` that focuses on a more specific area of expertise.
"""

import logging
from typing import Union

from django.db.models import QuerySet

from directory import models

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

        optional_args = f" with id: {subfunction_id}" if subfunction_id else "s"
        LOGGER.info(f"Fetching SubFunction{optional_args}.")
        # Please remove the ignore after implementation.
        return []  # type: ignore[return-value]
