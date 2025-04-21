"""
Collection of pytests for Portfolio's create controller.
"""

import pytest
from typing import cast, List

from django.contrib.auth import models as AuthModels
from django.test import tag

from program_review_tool import controllers, exceptions, models
from program_review_tool.controllers.Portfolio.tests.mutations.create.default import (
    arguments,
)
from program_review_tool.models.Portfolio.serializers import PortfolioSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "portfolio",
    "program_review_tool",
    "controllers.TestCreatePortfolio",
    "portfolio.create.default",
    "program_review_tool.portfolio.create",
)
class TestCreatePortfolio(MultiDBTestCase):
    """Test suite for Portfolio's create controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Portfolio/tests/mutations/create/default/fixtures/programs.json",
        "program_review_tool/controllers/Portfolio/tests/mutations/create/default/fixtures/portfolios.json",
    ]

    @tag("controllers.portfolio.create_portfolio")
    def test_create_portfolio(self) -> None:
        """Success Case: Create a `Portfolio` record."""

        # Query user from database.
        user = AuthModels.User.objects.get(
            username=arguments.CREATE_PORTFOLIO_USER_EMAIL
        )

        # Create portfolio for the user.
        portfolio = controllers.Portfolio.create_portfolio(
            user,
            name=arguments.CREATE_PORTFOLIO_NAME,
            programs=arguments.CREATE_PORTFOLIO_PROGRAM_IDS,
        )

        # Ensure data is a `Portfolio` instance.
        self.assertIsInstance(portfolio, models.Portfolio)

        data: dict = PortfolioSerializer(portfolio).data
        del data["created"]
        del data["modified"]

        # Ensure data is correct.
        self.assertDictEqual(data, arguments.CREATE_PORTFOLIO_EXPECTED_PORTFOLIO)

    @tag("controllers.portfolio.create_portfolio_user_not_authenticated")
    def test_create_portfolio_user_not_authenticated(self) -> None:
        """Fail Case: Create a `Portfolio` record with a `User`
        that is not authenticated."""

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Portfolio.create_portfolio(
                user=cast(AuthModels.User, AuthModels.AnonymousUser()),
                name=arguments.CREATE_PORTFOLIO_NAME,
                programs=arguments.CREATE_PORTFOLIO_PROGRAM_IDS,
            )

    @tag("controllers.portfolio.create_portfolio_empty_name")
    def test_create_portfolio_empty_name(self) -> None:
        """Fail Case: Create a `Portfolio` record with
        an empty name."""

        # Query user from database.
        user = AuthModels.User.objects.get(
            username=arguments.CREATE_PORTFOLIO_USER_EMAIL
        )

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Portfolio.create_portfolio(
                user=user,
                name="",
                programs=arguments.CREATE_PORTFOLIO_PROGRAM_IDS,
            )

    @tag("controllers.portfolio.create_portfolio_with_duplicate_name_for_user")
    def test_create_portfolio_with_duplicate_name_for_user(self) -> None:
        """Fail Case: Create a `Portfolio` record with a name
        that already exists for the given `User`."""

        # Query user from database.
        user = AuthModels.User.objects.get(
            username=arguments.CREATE_PORTFOLIO_USER_EMAIL
        )

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Portfolio.create_portfolio(
                user=user,
                name=arguments.CREATE_PORTFOLIO_DUPLICATE_NAME_FOR_USER,
                programs=arguments.CREATE_PORTFOLIO_PROGRAM_IDS,
            )

    @tag("controllers.portfolio.create_portfolio_empty_programs")
    def test_create_portfolio_empty_programs(self) -> None:
        """Fail Case: Create a `Portfolio` record without supplying
        `Program` ids."""

        # Query user from database.
        user = AuthModels.User.objects.get(
            username=arguments.CREATE_PORTFOLIO_USER_EMAIL
        )

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Portfolio.create_portfolio(
                user=user,
                name=arguments.CREATE_PORTFOLIO_NAME,
                programs=[],
            )

    @tag("controllers.portfolio.create_portfolio_programs_dne")
    def test_create_portfolio_programs_dne(self) -> None:
        """Fail Case: Create a `Portfolio` record, supplying
        ids for `Program`s that do not exist."""

        # Query user from database.
        user = AuthModels.User.objects.get(
            username=arguments.CREATE_PORTFOLIO_USER_EMAIL
        )

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Portfolio.create_portfolio(
                user=user,
                name=arguments.CREATE_PORTFOLIO_NAME,
                programs=arguments.CREATE_PORTFOLIO_PROGRAM_IDS_DNE,
            )
