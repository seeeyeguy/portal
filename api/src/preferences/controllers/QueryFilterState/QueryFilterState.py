"""
`BI Portal` `QueryFilterState` controller module. Controllers
utilize the Django ORM to create, fetch, and update records
within the `QueryFilterState` table. `QueryFilterState`
represents a user's preferred state of filters for the `BI Portal`
application.
"""

import logging
from typing import List

from preferences import models

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

        log_msg = (
            f"Creating QueryFilterState for user: {user} with search: {search}, "
            f"functions: {functions}, employee_levels: {employee_levels}, and "
            f"tags: {tags}."
        )
        LOGGER.info(log_msg)
        # Please remove the ignore after implementation.
        return {}  # type: ignore[return-value]

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
