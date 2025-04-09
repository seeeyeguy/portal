"""
Collection of pytests for Portfolio's fetch controller.
"""

from django.test import tag

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "portfolio",
    "program_review_tool",
    "controllers.TestFetchPortfolio",
    "portfolio.fetch.default",
    "program_review_tool.portfolio.fetch",
)
class TestFetchPortfolio(MultiDBTestCase):
    """Test suite for Portfolio's fetch controller."""

    @tag("controllers.portfolio.fetch_portfolios_by_user")
    def test_fetch_portfolios_by_user(self) -> None:
        """Success Case: Fetch all `Portfolio` records for
        the given user."""

    @tag("controllers.portfolio.fetch_portfolios_by_user_dne")
    def test_fetch_portfolios_by_user_dne(self) -> None:
        """Fail Case: Fetch all `Portfolio` records for
        a `User` that does not exist."""
