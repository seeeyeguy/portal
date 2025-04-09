"""
Collection of pytests for Resource's update controller.
"""

from django.test import tag

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

    @tag("controllers.portfolio.update_portfolio")
    def test_update_portfolio(self) -> None:
        """Success Case: Update a `Portfolio` record."""

    @tag("controllers.portfolio.update_portfolio_dne")
    def test_update_portfolio_dne(self) -> None:
        """Fail Case: Update a `Portfolio` record that
        does not exist."""

    @tag("controllers.portfolio.update_portfolio_empty_name")
    def test_update_portfolio_empty_name(self) -> None:
        """Fail Case: Update a `Portfolio` record with
        an empty name."""

    @tag("controllers.portfolio.update_portfolio_with_duplicate_name_for_user")
    def test_update_portfolio_with_duplicate_name_for_user(self) -> None:
        """Fail Case: Update a `Portfolio` record with a name
        that already exists for the given `User`."""

    @tag("controllers.portfolio.update_portfolio_empty_programs")
    def test_update_portfolio_empty_programs(self) -> None:
        """Fail Case: Update a `Portfolio` record without supplying
        `Program` ids."""

    @tag("controllers.portfolio.update_portfolio_programs_dne")
    def test_update_portfolio_programs_dne(self) -> None:
        """Fail Case: Update a `Portfolio` record supplying
        ids for `Program`s that do not exist."""
