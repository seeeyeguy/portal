"""
`BI Portal` `Usage` controller module. Controllers utilize the
Django ORM to create and fetch records within the `Usage` table.
`Usage` provides insights into the adoption of `Program Review Tool`.
"""

import logging
from typing import List, Optional
from datetime import datetime

from django.db.models import QuerySet
from django.contrib.auth import models as AuthModels

from program_review_tool import exceptions, models
from analytics import exceptions as analytics_exceptions

LOGGER = logging.getLogger(__name__)
DEFAULT_PAGE_LENGTH = 50


class Usage:
    """
    Container class for functions related to creating and
    retrieving `Usage` records. `Usage` provides insights
    into the adoption of `Program Review Tool`.
    """

    @staticmethod
    def create_usage(user: str, programs: List[str]) -> models.Usage:
        """
        Create a `Usage` record in the database given a user and
        program PA numbers.

        Accepts:
            * user (str): The user's email who executed the portfolio generation.
            * programs (List[str]): Program PA numbers used in the portfolio generation.

        Returns:
            * usage (models.Usage): The newly created `Usage` record.
        """

        try:
            LOGGER.info(f"Creating Usage for User: {user} with programs: {programs}.")

            # Fetch the `User` record.
            user_record: AuthModels.User = AuthModels.User.objects.get(
                email__iexact=user
            )

            # Create the `Query` record.
            usage: models.Usage = models.Usage.objects.create(
                user=user_record, programs=programs
            )

            return usage

        except AuthModels.User.DoesNotExist as exc:
            err_msg = f"User (email={user}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.ProgramReviewToolError(err_msg, 404) from exc

    @staticmethod
    def complete_usage(
        usage_id: int,
        success: bool,
        finish_time: datetime,
        error_msg: Optional[str] = None,
    ) -> models.Usage:
        """
        Complete a `Usage` record in the database given its id,
        success status. This is called after a portfolio generation is complete.

        Accepts:
            * id (int): The id of the `Usage` record to update.
            * success (bool): Was the portfolio generation successful.
            * duration (timedelta): How long it took to generate the portfolio.

        Returns:
            * usage (models.Usage): The updated `Usage` record.
        """

        try:
            LOGGER.info(f"Completing Usage with ID: {usage_id}, success: {success}.")

            # Fetch the `Usage` record.
            usage: models.Usage = models.Usage.objects.get(id=usage_id)

            # Check if the duration or success fields are already set
            if usage.duration is not None or usage.success is not None:
                # Return already completed `Usage`.
                return usage

            # Calculate the duration from the created time to now
            duration = finish_time - usage.created

            # Update the fields.
            usage.success = success
            usage.duration = duration
            if error_msg is not None:
                usage.error_msg = error_msg

            usage.save()

            return usage

        except models.Usage.DoesNotExist as exc:
            err_msg = f"Usage (id={usage_id}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.ProgramReviewToolError(err_msg, 404) from exc

    @staticmethod
    def fetch_usage(
        user: Optional[str] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        pa_number: Optional[str] = None,
        success: Optional[bool] = None,
    ) -> QuerySet[models.Usage]:
        """
        Fetch `Usage` records from the database given optional filters
        such as user and pagination parameters.

        Accepts:
            * user (str, optional): Filter usage records by the user's username
            * page (int, optional): The page number of results to return (must be positive).
            * limit (int, optional): The number of results per page (must be positive).
            * pa_number (str, optional): Filter usage records by Program PA number
            * success (bool, optional): Filter usage records by success (True) or failure (False)

        Returns:
            * usages (QuerySet[models.Usage]): A queryset of `Usage` records
            filtered and paginated according to the given arguments.
        """
        try:
            LOGGER.info(
                f"Fetching Usage — user: {user}, pa_number: {pa_number}, success: {success}, "
                f"page: {page}, limit: {limit}"
            )

            if page is not None and page < 1:
                raise analytics_exceptions.AnalyticsError(
                    "Page must be a positive integer.", 400
                )
            if limit is not None and limit < 1:
                raise analytics_exceptions.AnalyticsError(
                    "Limit must be a positive integer.", 400
                )

            # Base queryset: all Usage records ordered by creation time
            usages: QuerySet[models.Usage] = models.Usage.objects.select_related(
                "user"
            ).order_by("-created")

            # If `user` is provided, filter all queries by the given `User`
            if user:
                user_record: AuthModels.User = AuthModels.User.objects.get(
                    username__iexact=user
                )
                usages = usages.filter(user=user_record)

            # Filter by PA number (JSONField contains lookup)
            if pa_number:
                usages = usages.filter(programs__contains=[pa_number])

            # Filter by success/failure
            if success is not None:
                usages = usages.filter(success=success)

            # Apply pagination if both page and limit are provided
            if page is not None and limit is not None:
                start = (page - 1) * limit
                end = start + limit
                return usages[start:end]

            # Return full queryset if no pagination applied
            return usages
        # Catch any unexpected errors and raise a 500 ProgramReviewToolError
        except AuthModels.User.DoesNotExist as exc:
            msg = f"User (username={user}) does not exist."
            LOGGER.error(msg)
            raise analytics_exceptions.AnalyticsError(msg, 404) from exc
