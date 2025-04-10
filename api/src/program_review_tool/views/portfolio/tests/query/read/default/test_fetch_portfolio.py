"""
Collection of pytests for Portfolio's fetch view endpoint.
"""

from django.test import tag
from django.urls import reverse

from manager.utils.tests import MultiDBTestCase


@tag(
    "portfolio",
    "program_review_tool",
    "views",
    "portfolio.fetch.default",
    "program_review_tool.portfolio.fetch",
    "views.TestFetchPortfolio",
)
class TestFetchPortfolio(MultiDBTestCase):
    """
    Tests for GET /v1/program-review-tool/portfolio endpoint.
    """

    url: str = reverse("program_review_tool.portfolio")

    @tag("views.portfolio.fetch_portfolios_by_user")
    def test_fetch_portfolios_by_user(self) -> None:
        """Success Case: Fetch all `Portfolio` records for
        the given user."""

    @tag("views.portfolio.fetch_portfolios_by_user_dne")
    def test_fetch_portfolios_by_user_dne(self) -> None:
        """Fail Case: Fetch all `Portfolio` records for
        a `User` that does not exist."""
