"""
`BI Portal` `QueryFilterState` controller module. Controllers
utilize the Django ORM to create, fetch, and update records
within the `QueryFilterState` table. `QueryFilterState`
represents a user's preferred state of filters for the `BI Portal`
application.
"""

import logging
from typing import List

from django.contrib.auth.models import User
from django.db.models import QuerySet

from analytics import models as AnalyticsModels
from directory import models as DirectoryModels
from preferences import exceptions, models

LOGGER = logging.getLogger(__name__)


class QueryFilterState:
    """
    Container class for functions related to creating, updating,
    and retrieving `QueryFilterState` records. `QueryFilterState`
    represents a user's preferred state of filters for the `BI Portal`
    application.
    """

    @staticmethod
    def create_query_filter_state(
        user: str,
        search: int,
        functions: List[int],
        employee_levels: List[int],
        tags: List[int],
    ) -> models.QueryFilterState:
        """
        Create `QueryFilterState` record in the database for the given user,
        search, functions, employee_levels, and tags.

        Accepts:
            * user (str): Email for the user related to this `QueryFilterState`.
            * search (int): Id of a search query made by the user.
            * functions (List[int]): Ids of `Function`s selected by the user.
            * employee_levels (List[int]): Ids of `EmployeeLevel`s selected by the user.
            * tags (List[int]): Ids of `Tag`s for resources selected by the user.

        Returns:
            * query_filter_state (models.QueryFilterState): The newly created
                `QueryFilterState` record.
        """

        try:
            log_msg = (
                f"Creating QueryFilterState for user: {user} with search: {search}, "
                f"functions: {functions}, employee_levels: {employee_levels}, and "
                f"tags: {tags}."
            )
            LOGGER.info(log_msg)

            # Fetch `User` record.
            user_record: User = User.objects.get(email__iexact=user)

            # Ensure `QueryFilterState` doesn't already exist for the `User`.
            if models.QueryFilterState.objects.filter(user=user_record).exists():
                err_msg = f"User (email={user}) may only have one search & filter session state."
                LOGGER.error(err_msg)
                raise exceptions.PreferencesError(err_msg, 400)

            # Fetch `Query` record.
            query_record: AnalyticsModels.Query | None = (
                AnalyticsModels.Query.objects.get(id=search) if search else None
            )

            # Fetch `Function` records.
            function_records: QuerySet[
                DirectoryModels.Function
            ] = DirectoryModels.Function.objects.filter(id__in=functions)
            if function_records.count() != len(functions):
                err_msg = f"Some Functions (ids={functions}) do not exist."
                LOGGER.error(err_msg)
                raise exceptions.PreferencesError(err_msg, 404)

            # Fetch `EmployeeLevel` records.
            employee_level_records: QuerySet[
                DirectoryModels.EmployeeLevel
            ] = DirectoryModels.EmployeeLevel.objects.filter(id__in=employee_levels)
            if employee_level_records.count() != len(employee_levels):
                err_msg = f"Some EmployeeLevels (ids={employee_levels}) do not exist."
                LOGGER.error(err_msg)
                raise exceptions.PreferencesError(err_msg, 404)

            # Fetch `Tag` records.
            tag_records: QuerySet[
                DirectoryModels.Tag
            ] = DirectoryModels.Tag.objects.filter(id__in=tags)
            if tag_records.count() != len(tags):
                err_msg = f"Some Tags (ids={tags}) do not exist."
                LOGGER.error(err_msg)
                raise exceptions.PreferencesError(err_msg, 404)

            # Create `QueryFilterState` record.
            query_filter_state: models.QueryFilterState = (
                models.QueryFilterState.objects.create(
                    search=query_record,
                    user=user_record,
                )
            )

            # Add `Function`s, `EmployeeLevel`s, and `Tag`s.
            query_filter_state.functions.add(*function_records)
            query_filter_state.employee_levels.add(*employee_level_records)
            query_filter_state.tags.add(*tag_records)

            return query_filter_state
        except User.DoesNotExist as exc:
            err_msg = f"User (email={user}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.PreferencesError(err_msg, 404) from exc
        except AnalyticsModels.Query.DoesNotExist as exc:
            err_msg = f"Query (id={search}) does not exist."
            LOGGER.error(err_msg)
            raise exceptions.PreferencesError(err_msg, 404) from exc

    @staticmethod
    def update_query_filter_state(
        record_id: int,
        search: int,
        functions: List[int],
        employee_levels: List[int],
        tags: List[int],
    ) -> models.QueryFilterState:
        """
        Update `QueryFilterState` record for the given id with the given
        search, functions, employee_levels, and tags.

        Accepts:
            * id (int): Id of the `QueryFilterState` record to be updated.
            * search (int): Id of a search query made by the user.
            * functions (List[int]): Ids of `Function`s selected by the user.
            * employee_levels (List[int]): Ids of `EmployeeLevel`s selected by the user.
            * tags (List[int]): Ids of `Tag`s for resources selected by the user.

        Returns:
            * query_filter_state (models.QueryFilterState): Updated `QueryFilterState`
                record based on the user's provided parameters.
        """

        log_msg = (
            f"Updating QueryFilterState with id: {record_id} with search: {search}, "
            f"functions: {functions}, employee_levels: {employee_levels}, and "
            f"tags: {tags}."
        )
        LOGGER.info(log_msg)
        # Please remove the ignore after implementation.
        return {}  # type: ignore[return-value]

    @staticmethod
    def fetch_query_filter_state(user: str) -> models.QueryFilterState:
        """
        Fetch the `QueryFilterState` record for the given user.

        Accepts:
            * user (str): Email for the user related to this `QueryFilterState`.

        Returns:
            * query_filter_state (models.QueryFilterState): The `QueryFilterState`
                record for the given user.
        """

        LOGGER.info(f"Fetching QueryFilterState for user: {user}.")
        # Please remove the ignore after implementation.
        return {}  # type: ignore[return-value]
