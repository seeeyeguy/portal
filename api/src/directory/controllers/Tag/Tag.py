"""
`BI Portal` `Tag` controller module. Controllers utilize the
Django ORM to fetch records within the `Tag` table. `Tag`
helps to categorize resources through keywords represented
by labels.
"""

import logging
from typing import Union

from django.db.models import QuerySet

from directory import models

LOGGER = logging.getLogger(__name__)


class Tag:
    """
    Container class for functions related to retrieving and
    searching `Tag` records. `Tag` helps to categorize resources
    through keywords represented by labels.
    """

    @staticmethod
    def fetch_tags(
        tag_id: int | None = None, page: int | None = None, limit: int | None = None
    ) -> Union[models.Tag, QuerySet[models.Tag]]:
        """
        Fetch a `Tag` object from the database with the given
        id or if no id is specified return all `Tag` objects.
        If page is specified, return the page of records. If
        limit is specified, return `limit` number of records.

        Accepts:
            * tag_id (int | None): Optional parameter to either return a
                single `Tag` object with the specified id or all
                `Tag` objects in the database.
            * page (int | None): The page of `Tag` records to return.
            * limit (int | None): The limit of `Tag` records to return.

        Returns:
            * tags (Union[models.Tag, QuerySet[models.Tag]]):
                Either one `Tag` instance with the specified id
                or a QuerySet of all `Tag` instances.
        """

        optional_args = f" with id: {tag_id}" if tag_id else "s"
        optional_args = f"{optional_args} with page: {page}" if page else optional_args
        optional_args = (
            f"{optional_args}{' and ' if page else ' with '}limit: {limit}"
            if limit
            else optional_args
        )
        LOGGER.info(f"Fetching Tag{optional_args}.")
        # Please remove the ignore after implementation.
        return []  # type: ignore[return-value]

    @staticmethod
    def search_tags(
        label: str,
    ) -> QuerySet[models.Tag]:
        """
        Search for `Tag` instances in the database that match the
        provided label using a `startswith` style search.

        Accepts:
            * label (str): Label that will be used to search for
                `Tag` instances.

        Returns:
            * (QuerySet[models.Tag]): A QuerySet of `Tag` instances
                that match the provided search label.
        """

        LOGGER.info(f"Searching for Tags with label: {label}.")

        return models.Tag.objects.filter(label__istartswith=label)
