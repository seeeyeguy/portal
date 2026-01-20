"""
Collection of pytests for Portfolio's delete controller.
"""

import pytest
from typing import cast, List

# pylint: disable=line-too-long
from django.contrib.auth import models as AuthModels
from django.test import tag

from program_review_tool import controllers, exceptions
from program_review_tool.controllers.Portfolio.tests.mutations.delete.default import (
    arguments,
)

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "portfolio",
    "program_review_tool",
    "controllers.TestDeletePortfolio",
    "portfolio.delete.default",
    "program_review_tool.portfolio.delete",
)
class TestDeletePortfolio(MultiDBTestCase):
    """Test suite for Portfolio's delete controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Portfolio/tests/mutations/delete/default/fixtures/programs.json",
        "program_review_tool/controllers/Portfolio/tests/mutations/delete/default/fixtures/portfolios.json",
    ]

    @tag("controllers.portfolio.delete_portfolio")
    def test_delete_portfolio(self) -> None:
        """Success Case: Delete `Portfolio` record with the given id."""

        user = AuthModels.User.objects.get(
            username=arguments.DELETE_PORTFOLIO_USER_EMAIL
        )
        rows_affected = controllers.Portfolio.delete_portfolio(
            portfolio_id=arguments.DELETE_PORTFOLIO_PORTFOLIO_ID, user=user
        )
        self.assertEqual(rows_affected, arguments.EXPECTED_ROWS_AFFECTED)

    @tag("controllers.portfolio.delete_portfolio_user_not_authenticated")
    def test_delete_portfolio_user_not_authenticated(self) -> None:
        """Fail Case: Delete `Portfolio` record for a `User`
        that is not authenticated."""

        user = cast(AuthModels.User, AuthModels.AnonymousUser())
        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Portfolio.delete_portfolio(
                portfolio_id=arguments.DELETE_PORTFOLIO_PORTFOLIO_ID, user=user
            )

    @tag("controllers.portfolio.delete_portfolio_permissions_denied")
    def test_delete_portfolio_permissions_denied(self) -> None:
        """Fail Case: Delete `Portfolio` record for the wrong user."""

        user = AuthModels.User.objects.get(
            username=arguments.DELETE_PORTFOLIO_USER_EMAIL_PERMISSIONS_DENIED
        )
        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Portfolio.delete_portfolio(
                portfolio_id=arguments.DELETE_PORTFOLIO_PORTFOLIO_ID, user=user
            )
