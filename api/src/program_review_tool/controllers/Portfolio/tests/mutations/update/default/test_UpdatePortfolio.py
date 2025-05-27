"""
Collection of pytests for Resource's update controller.
"""

import pytest
from typing import cast, List

from django.contrib.auth import models as AuthModels
from django.test import tag

from program_review_tool import controllers, exceptions, models
from program_review_tool.controllers.Portfolio.tests.mutations.update.default import (
    arguments,
)
from program_review_tool.models.Portfolio.serializers import PortfolioSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "portfolio",
    "program_review_tool",
    "controllers.TestUpdatePortfolio",
    "portfolio.update.default",
    "program_review_tool.portfolio.update",
)
class TestUpdatePortfolio(MultiDBTestCase):
    """Test suite for Portfolio's update controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Portfolio/tests/mutations/update/default/fixtures/portfolios.json",
        "program_review_tool/controllers/Portfolio/tests/mutations/update/default/fixtures/programs.json",
        "program_review_tool/controllers/Portfolio/tests/mutations/update/default/fixtures/segments.json",
    ]

    @tag("controllers.portfolio.update_portfolio")
    def test_update_portfolio(self) -> None:
        """Success Case: Update a `Portfolio` record."""

        # Query user from database.
        user = AuthModels.User.objects.get(
            username=arguments.UPDATE_PORTFOLIO_USER_EMAIL
        )

        # Update portfolio for the user.
        portfolio, rows_affected = controllers.Portfolio.update_portfolio(
            portfolio_id=arguments.UPDATE_PORTFOLIO_PORTFOLIO_ID,
            user=user,
            name=arguments.UPDATE_PORTFOLIO_PORTFOLIO_NAME,
            programs=arguments.UPDATE_PORTFOLIO_PROGRAM_IDS,
        )

        # Ensure data is a `Portfolio` instance.
        self.assertIsInstance(portfolio, models.Portfolio)

        self.assertEqual(
            rows_affected, arguments.UPDATE_PORTFOLIO_EXPECTED_ROWS_AFFECTED
        )

        data: dict = PortfolioSerializer(portfolio).data

        del data["created"]
        del data["modified"]

        # Ensure data is correct.
        self.assertDictEqual(data, arguments.UPDATE_PORTFOLIO_EXPECTED_PORTFOLIO)

    @tag("controllers.portfolio.update_portfolio_user_not_authenticated")
    def test_update_portfolio_user_not_authenticated(self) -> None:
        """Fail Case: Update a `Portfolio` record with a `User`
        that is not authenticated."""

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Portfolio.update_portfolio(
                portfolio_id=arguments.UPDATE_PORTFOLIO_PORTFOLIO_ID,
                user=cast(AuthModels.User, AuthModels.AnonymousUser()),
                name=arguments.UPDATE_PORTFOLIO_PORTFOLIO_NAME,
                programs=arguments.UPDATE_PORTFOLIO_PROGRAM_IDS,
            )

    @tag("controllers.portfolio.update_portfolio_portfolio_dne")
    def test_update_portfolio_portfolio_dne(self) -> None:
        """Fail Case: Update a `Portfolio` record that
        does not exist."""

        # Query user from database.
        user = AuthModels.User.objects.get(
            username=arguments.UPDATE_PORTFOLIO_USER_EMAIL
        )

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Portfolio.update_portfolio(
                portfolio_id=arguments.UPDATE_PORTFOLIO_PORTFOLIO_ID_DNE,
                user=user,
                name=arguments.UPDATE_PORTFOLIO_PORTFOLIO_NAME,
                programs=arguments.UPDATE_PORTFOLIO_PROGRAM_IDS,
            )

    @tag("controllers.portfolio.update_portfolio_empty_name")
    def test_update_portfolio_empty_name(self) -> None:
        """Fail Case: Update a `Portfolio` record with
        an empty name."""

        # Query user from database.
        user = AuthModels.User.objects.get(
            username=arguments.UPDATE_PORTFOLIO_USER_EMAIL
        )

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Portfolio.update_portfolio(
                portfolio_id=arguments.UPDATE_PORTFOLIO_PORTFOLIO_ID,
                user=user,
                name="",
                programs=arguments.UPDATE_PORTFOLIO_PROGRAM_IDS,
            )

    @tag("controllers.portfolio.update_portfolio_empty_programs")
    def test_update_portfolio_empty_programs(self) -> None:
        """Fail Case: Update a `Portfolio` record without supplying
        `Program` ids."""

        # Query user from database.
        user = AuthModels.User.objects.get(
            username=arguments.UPDATE_PORTFOLIO_USER_EMAIL
        )

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Portfolio.update_portfolio(
                portfolio_id=arguments.UPDATE_PORTFOLIO_PORTFOLIO_ID,
                user=user,
                name=arguments.UPDATE_PORTFOLIO_PORTFOLIO_NAME,
                programs=[],
            )

    @tag("controllers.portfolio.update_portfolio_programs_dne")
    def test_update_portfolio_programs_dne(self) -> None:
        """Fail Case: Update a `Portfolio` record, supplying
        ids for `Program`s that do not exist."""

        # Query user from database.
        user = AuthModels.User.objects.get(
            username=arguments.UPDATE_PORTFOLIO_USER_EMAIL
        )

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Portfolio.update_portfolio(
                portfolio_id=arguments.UPDATE_PORTFOLIO_PORTFOLIO_ID,
                user=user,
                name=arguments.UPDATE_PORTFOLIO_PORTFOLIO_NAME,
                programs=arguments.UPDATE_PORTFOLIO_PROGRAM_IDS_DNE,
            )

    @tag(
        "controllers.portfolio.update_portfolio_with_duplicate_portfolio_name_for_user"
    )
    def test_update_portfolio_with_duplicate_portfolio_name_for_user(self) -> None:
        """Fail Case: Update a `Portfolio` record with a name
        that already exists for another record for the given `User`."""

        # Query user from database.
        user = AuthModels.User.objects.get(
            username=arguments.UPDATE_PORTFOLIO_USER_EMAIL
        )

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Portfolio.update_portfolio(
                portfolio_id=arguments.UPDATE_PORTFOLIO_DUPLICATE_PORTFOLIO_NAME_FOR_USER_PORTFOLIO_ID,
                user=user,
                name=arguments.UPDATE_PORTFOLIO_DUPLICATE_PORTFOLIO_NAME_FOR_USER,
                programs=arguments.UPDATE_PORTFOLIO_PROGRAM_IDS,
            )
