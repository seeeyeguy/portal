"""
`BI Portal` `Tag` controller module. Controllers utilize the
Django ORM to fetch records within the `Tag` table. `Tag`
helps to categorize resources through keywords represented
by labels.
"""

import logging
from typing import cast, Union

from django.core.paginator import Page, Paginator
from django.db.models import QuerySet

from directory import exceptions, models

LOGGER = logging.getLogger(__name__)

# Default page length used when using
# pagination on the fetch.
DEFAULT_PAGE_LENGTH: int = 50


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

        try:
            optional_args = f" with id: {tag_id}" if tag_id else "s"
            optional_args = (
                f"{optional_args} with page: {page}" if page else optional_args
            )
            optional_args = (
                f"{optional_args}{' and ' if page else ' with '}limit: {limit}"
                if limit
                else optional_args
            )
            LOGGER.info(f"Fetching Tag{optional_args}.")

            # If tag id is given, along with either a page
            # or limit then throw an invalid parameters error.
            if tag_id and (page or limit):
                raise exceptions.DirectoryError("Invalid parameters given.", 400)

            # If a tag id is given, fetch the corresponding `Tag` record,
            # else all `Tag` records.
            tags: Union[models.Tag, QuerySet[models.Tag]] = (
                models.Tag.objects.get(id=tag_id)
                if tag_id
                else models.Tag.objects.all()
            )

            # If `limit` is given, then limit the `Tag` records.
            tags = tags[:limit] if limit else tags  # type: ignore[index]

            if page:
                # Create a Paginator to paginate the collection
                # of `Tag`s.
                # pylint: disable=line-too-long
                paginator: Paginator = Paginator(tags, DEFAULT_PAGE_LENGTH)  # type: ignore[arg-type]

                # If `page` number supplied in the params is greater
                # than the number of available pages, then return an
                # empty `Tag` QuerySet.
                if page > paginator.num_pages:
                    return models.Tag.objects.none()

                # Get the corresponding Page.
                tag_page: Page = paginator.page(page)

                # Assign the page's `Tag` QuerySet to
                # `tags`.
                tags = cast(QuerySet[models.Tag], tag_page.object_list)

            return tags
        except models.Tag.DoesNotExist as exc:
            err_msg = f"Tag (id={tag_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, 404) from exc

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
