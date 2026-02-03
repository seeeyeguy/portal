"""
`BI Portal` `Content` controller module. Controllers create,
fetch, update, and delete records within the `Content` table.
`Content` is the dynamic content served by `BI Portal` and
may take any form that is JSON compliant.
"""

import logging
from typing import Set

from django.contrib.auth.models import User
from django.db import DatabaseError
from django.utils import timezone

from content import exceptions, models
from users.models import Role

LOGGER = logging.getLogger(__name__)

# Valid `Role` levels.
VALID_ROLE_LEVELS: Set[int] = {
    Role.RoleLevels.SUPERUSER,
}


class Content:
    """
    Container class for functions related creating, updating, retrieving
    and deleting `Content` records. `Content` is the dynamic content
    served by `BI Portal` and may take any form that is JSON
    compliant.
    """

    @staticmethod
    def create_content(key: str, content: dict, created_by: User) -> models.Content:
        """
        Create a `Content` record with the given params.

        Accepts:
          * key (str): An alias for dynamic content.
          * content (dict): JSON compliant dynamic content for `BI Portal`.
          * created_by (auth.User): The user that created the content.

        Returns:
          * content (models.Content): The `Content` record created.
        """

        log_message = (
            f"Creating Content(key={key},"
            f" content={content}, modified_by={created_by}) record."
        )

        try:
            LOGGER.info(log_message)

            # Verify user has an `Access` with a valid Role.
            if not created_by.accesses.filter(
                access_revoked_date__isnull=True, role__level__in=VALID_ROLE_LEVELS
            ).exists():
                err_msg = "Permissions Denied."
                LOGGER.error(err_msg)
                raise exceptions.ContentError(err_msg, 403)

            # Create record.
            content: models.Content = models.Content.objects.create(
                key=key,
                content=content,
                created=timezone.now(),
                modified=timezone.now(),
                modified_by=created_by,
            )

            return content
        except DatabaseError as exc:
            error_message = (
                f"Content(key={key},"
                f" content={content}, modified_by={created_by}) record not created."
                f" Please check params. {exc}"
            )
            LOGGER.error(error_message)
            raise exceptions.ContentError(error_message, status=400) from exc

    @staticmethod
    def fetch_content(key: str) -> models.Content:
        """
        Fetch a `Content` record with the given key.

        Accepts:
            * key (str): The unique alias for the `Content` record.

        Returns:
            * record (models.Content): A `Content` record.
        """

        log_message = f"Fetching Content(key={key}) record."

        try:
            LOGGER.info(log_message)
            record = models.Content.objects.get(key=key)
            return record
        except models.Content.DoesNotExist as exc:
            error_message = f"Content(key={key}) does not exist."
            LOGGER.error(error_message)
            raise exceptions.ContentError(error_message, status=404) from exc

    @staticmethod
    def delete_content(key: str, deleted_by: User) -> int:
        """
        Delete a `Content` record with the given key.

        Accepts:
            * key (str): The unique alias for the `Content` record.
            * deleted_by (auth.User): The user that deleted the content.

        Returns:
            * rows_affected (int): The number of rows deleted.
        """

        log_message = f"Deleting Content(key={key}) record."

        LOGGER.info(log_message)

        # Verify user has an `Access` with a valid Role.
        if not deleted_by.accesses.filter(
            access_revoked_date__isnull=True, role__level__in=VALID_ROLE_LEVELS
        ).exists():
            err_msg = "Permissions Denied."
            LOGGER.error(err_msg)
            raise exceptions.ContentError(err_msg, 403)

        rows_affected, _ = models.Content.objects.filter(key=key).delete()
        return rows_affected
