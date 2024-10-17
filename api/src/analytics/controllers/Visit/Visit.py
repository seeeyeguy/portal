"""
`BI Portal` `Visit` controller module. Controllers utilize the
Django ORM to create and fetch records within the `Visit` table.
`Visit` provides insights into users' behavior, particularly in
regards to the use of resources.
"""

import logging
from typing import Union

from django.db.models import QuerySet
from django.contrib.auth import models as AuthModels

from analytics import exceptions, models
from directory import models as DirectoryModels

LOGGER = logging.getLogger(__name__)


class Visit:
    """
    Container class for functions related to creating and
    retrieving `Visit` records. `Visit` provides insights
    into users' behavior, particularly in regards to the
    use of resources.
    """

    @staticmethod
    def create_visit(user: str, resource: int) -> models.Visit:
        """
        Create a `Visit` record in the database given a user and
        resource id.

        Accepts:
            * user (str): The user's email who visited a given resource.
            * resource (int): The id of the resource that is being visited.

        Returns:
            * visit (models.Visit): The newly created `Visit` record.
        """

        try:
            LOGGER.info(
                f"Creating Visit for User: {user} and Resource with id: {resource}."
            )

            # Fetch the `User` record.
            user_record: AuthModels.User = AuthModels.User.objects.get(
                email__iexact=user
            )

            # Fetch the `Resource` record.
            resource_record: DirectoryModels.Resource = (
                DirectoryModels.Resource.objects.get(id=resource)
            )

            # Create the `Visit` record.
            visit = models.Visit.objects.create(
                user=user_record, resource=resource_record
            )
            return visit
        except AuthModels.User.DoesNotExist as exc:
            err_msg = f"User (email={user}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.AnalyticsError(err_msg, 404) from exc

        except DirectoryModels.Resource.DoesNotExist as exc:
            err_msg = f"Resource (id={resource}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.AnalyticsError(err_msg, 404) from exc

    @staticmethod
    def fetch_visit(
        record_id: int | None,
        user: str,
        resource: int | None,
        page: int | None = None,
        limit: int | None = None,
    ) -> Union[models.Visit, QuerySet[models.Visit]]:
        """
        Fetch all `Visit` records based on the arguments passed to this
        controller. If page, limit, user, or resource are specified then
        a QuerySet of `Visit` records will be returned matching the
        arguments. If an id is specified then the associated `Visit` record
        will be returned.

        Accepts:
            * record_id (int | None): The id of the `Visit` record.
            * user (str): The user associated with the `Visit`.
            * resource (int | None): The id of the `Resource` associated
                with the `Visit`.
            * page (int | None): The page of `Visit` records to return.
            * limit (int | None): The limit of `Visit` records to return.

        Returns:
            *visits (Union[models.Visit, QuerySet[models.Visit]]): The
                `Visit` records based on the given arguments.
        """

        optional_args = f" with record_id: {record_id}" if record_id else "s"
        optional_args = f" for User: {user}" if user != "" else optional_args
        optional_args = (
            f" {optional_args} with resource: {resource}" if resource else optional_args
        )
        optional_args = f" {optional_args} with page: {page}" if page else optional_args
        optional_args = (
            f"{optional_args}{' and ' if page else 'with '}limit: {limit}"
            if limit
            else optional_args
        )

        LOGGER.info(f"Fetching `Visit`{optional_args}.")
        # Please remove the ignore after implementation.
        return []  # type: ignore[return-value]
