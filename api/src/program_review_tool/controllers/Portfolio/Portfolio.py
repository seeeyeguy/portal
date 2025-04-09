"""
`Program Review Tool` `Portfolio` controller module. Controllers utilize the
Django ORM to create, fetch, update, and delete records within
the `Portfolio` table.
"""

import logging
from typing import List

from django.contrib.auth import models as AuthModels
from django.db.models import QuerySet

from program_review_tool import models

LOGGER = logging.getLogger(__name__)


class Portfolio:
    """
    Container class for functions related to creating, updating,
    retrieving, and deleting `Portfolio` records.
    """

    # pylint: disable=line-too-long
    @staticmethod
    def create_portfolio(
        user: AuthModels.User, name: str, programs: List[int]
    ) -> models.Portfolio:
        """
        Create a `Portfolio` record in the database using the given
        user, name and program ids.

        Accepts:
            * user (AuthModels.User): The `User` that is creating the portfolio.
            * name (str): The name of the portfolio.
            * programs (List[int]): The ids of the `Program`s being linked
                to the portfolio.

        Returns:
            * portfolio (models.Portfolio): The newly created `Portfolio`
                record.
        """

        LOGGER.info(
            (
                f"Creating Portfolio with name: {name} and Programs:{programs} "
                f"for user: {user.email}"
            )
        )

        # Please remove ignore after implementation.
        return {}  # type: ignore[return-value]

    # pylint: disable=line-too-long
    @staticmethod
    def update_portfolio(
        portfolio_id: int, name: str, programs: List[int]
    ) -> models.Portfolio:
        """
        Update a `Portfolio` record for the given id with the given params.

        Accepts:
            * portfolio_id (int): The id of the portfolio being updated.
            * name (str): The name being updated on the portfolio.
            * programs (List[int]): The ids of the `Program`s being linked
                to the portfolio.

        Returns:
            * portfolio (models.Portfolio): The updated `Portfolio` record.
            * rows_affected (int): The number of `Portfolio` records updated.
        """

        LOGGER.info(
            (
                f"Updating Portfolio(id={portfolio_id}) with name: {name} "
                f"and Programs:{programs}"
            )
        )

        # Please remove ignore after implementation.
        return {}  # type: ignore[return-value]

    @staticmethod
    def delete_portfolio(portfolio_id: int) -> int:
        """
        Delete the `Portfolio` record with the given id.

        Accepts:
            * portfolio_id (int): The id of the `Portfolio` record being deleted.

        Returns:
            * rows_affected (int): Number of rows removed.
        """

        LOGGER.info(f"Deleting Portfolio instance with id: {portfolio_id}.")

        return 1

    @staticmethod
    def fetch_portfolios(user: AuthModels.User) -> QuerySet[models.Portfolio]:
        """
        Fetch all `Portfolio` records for the given user.

        Accepts:
            * user (AuthModels.User): The `User` related to the
                `Portfolio` records.

        Returns:
            portfolios (QuerySet[models.Portfolio]): All `Portfolio`
                records for the given user.
        """

        LOGGER.info(f"Fetching Portfolios for user: {user.email}")

        # Please remove ignore after implementation.
        return {}  # type: ignore[return-value]
