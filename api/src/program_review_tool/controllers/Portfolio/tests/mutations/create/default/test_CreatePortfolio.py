"""
Collection of pytests for Portfolio's create controller.
"""

from django.test import tag

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

    @tag("controllers.portfolio.create_portfolio")
    def test_create_portfolio(self) -> None:
        """Success Case: Create a `Portfolio` record."""

    @tag("controllers.portfolio.create_portfolio_user_dne")
    def test_create_portfolio_user_dne(self) -> None:
        """Fail Case: Create a `Portfolio` record with a `User`
        that does not exist."""

    @tag("controllers.portfolio.create_portfolio_empty_name")
    def test_create_portfolio_empty_name(self) -> None:
        """Fail Case: Create a `Portfolio` record with
        an empty name."""

    @tag("controllers.portfolio.create_portfolio_with_duplicate_name_for_user")
    def test_create_portfolio_with_duplicate_name_for_user(self) -> None:
        """Fail Case: Create a `Portfolio` record with a name
        that already exists for the given `User`."""

    @tag("controllers.portfolio.create_portfolio_empty_programs")
    def test_create_portfolio_empty_programs(self) -> None:
        """Fail Case: Create a `Portfolio` record without supplying
        `Program` ids."""

    @tag("controllers.portfolio.create_portfolio_programs_dne")
    def test_create_portfolio_programs_dne(self) -> None:
        """Fail Case: Create a `Portfolio` record supplying
        ids for `Program`s that do not exist."""
