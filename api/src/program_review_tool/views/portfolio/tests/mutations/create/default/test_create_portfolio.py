"""
Collection of pytests for Portfolio's create view endpoint.
"""

from django.test import tag
from django.urls import reverse

from manager.utils.tests import MultiDBTestCase


@tag(
    "portfolio",
    "program_review_tool",
    "views",
    "portfolio.create.default",
    "program_review_tool.portfolio.create",
    "views.TestCreatePortfolio",
)
class TestCreatePortfolio(MultiDBTestCase):
    """
    Tests for POST /v1/program-review-tool/portfolio endpoint.
    """

    url: str = reverse("program_review_tool.portfolio")

    @tag("views.portfolio.create_portfolio")
    def test_create_portfolio(self) -> None:
        """Success Case: Create a `Portfolio` record."""

    @tag("views.portfolio.create_portfolio_user_dne")
    def test_create_portfolio_user_dne(self) -> None:
        """Fail Case: Create a `Portfolio` record with a `User`
        that does not exist."""

    @tag("views.portfolio.create_portfolio_empty_name")
    def test_create_portfolio_empty_name(self) -> None:
        """Fail Case: Create a `Portfolio` record with
        an empty name."""

    @tag("views.portfolio.test_create_portfolio_duplicate_name")
    def test_create_portfolio_duplicate_name(self) -> None:
        """Fail Case: Create a `Portfolio` record with
        a duplicate name for the given user."""

    @tag("views.portfolio.create_portfolio_empty_programs")
    def test_create_portfolio_empty_programs(self) -> None:
        """Fail Case: Create a `Portfolio` record without supplying
        `Program` ids."""

    @tag("views.portfolio.create_portfolio_programs_dne")
    def test_create_portfolio_programs_dne(self) -> None:
        """Fail Case: Create a `Portfolio` record, supplying
        ids for `Program`s that do not exist."""
