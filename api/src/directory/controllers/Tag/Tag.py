"""
`BI Portal` `Tag` controller module. Controllers utilize the
Django ORM to fetch records within the `Tag` table. `Tag`
helps to categorize resources through keywords represented
by labels.
"""

import logging
from typing import cast, Tuple, Union

from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from django.utils import timezone

from directory import exceptions, models

LOGGER = logging.getLogger(__name__)

# Default page length used when using
# pagination on the fetch.
DEFAULT_PAGE_LENGTH: int = 50


class Tag:
    """
    Container class for functions related to creating, updating,
    deleting, retrieving, and searching `Tag` records. `Tag`
    helps to categorize resources through keywords represented
    by labels.
    """

    @staticmethod
    def create_tag(label: str) -> models.Tag:
        """
        Create a `Tag` record with the given label.

        Accepts:
            * label (str): An arbitrary keyword, created by an admin.

        Returns:
            * tag (models.Tag): The `Tag` record created.
        """

        LOGGER.info(f"Creating Tag with label: {label}.")

        if models.Tag.objects.filter(label=label).exists():
            err_msg = f"A Tag with the given label: ({label}) already exists."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, 400)

        tag_record = models.Tag.objects.create(label=label)
        return tag_record

    @staticmethod
    def update_tag(tag_id: int, label: str) -> Tuple[models.Tag, int]:
        """
        Update a `Tag` record for the given id with the given label.

        Accepts:
            * tag_id (int): The id of the record to be updated.
            * label (str): An arbitrary keyword, created by an admin.

        Returns:
            * tag (models.Tag): The `Tag` record updated.
            * rows_affected (int): Number of rows affected.
        """

        try:
            LOGGER.info(f"Updating Tag with id: {tag_id} with label: {label}.")

            # Fetch `Tag` record by id.
            tag_record: models.Tag = models.Tag.objects.get(id=tag_id)

            # Check for existing `Tag` with given label, excluding
            # the target `Tag`.
            if (
                models.Tag.objects.filter(label__iexact=label)
                .exclude(id=tag_id)
                .exists()
            ):
                raise exceptions.DirectoryError(
                    f"Tag (label={label}) already exists.", 400
                )

            # Update the `Tag` record.
            rows_affected = models.Tag.objects.filter(id=tag_id).update(
                label=label, modified=timezone.now()
            )
            tag_record.refresh_from_db()

            return tag_record, rows_affected
        except models.Tag.DoesNotExist as exc:
            err_msg = f"Tag (id={tag_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.DirectoryError(err_msg, 404) from exc

    @staticmethod
    def delete_tag(tag_id: int) -> int:
        """
        Delete a `Tag` record with the given id.

        Accepts:
            * tag_id (int): The id of the record to be deleted.

        Returns:
            * rows_affected (int): The number of rows removed.
        """

        LOGGER.info(f"Deleting Tag with id: {tag_id}.")

        # Query the corresponding `Tag` record with the given id.
        tag_query: QuerySet[models.Tag] = models.Tag.objects.filter(id=tag_id)

        # Delete `Tag` record.
        rows_affected, _ = tag_query.delete()

        return rows_affected

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
