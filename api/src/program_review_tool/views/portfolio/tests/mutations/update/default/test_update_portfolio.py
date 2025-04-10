"""
Collection of pytests for Portfolio's update view endpoint.
"""

from django.test import tag
from django.urls import reverse

from manager.utils.tests import MultiDBTestCase


@tag(
    "portfolio",
    "program_review_tool",
    "views",
    "portfolio.update.default",
    "program_review_tool.portfolio.update",
    "views.TestUpdatePortfolio",
)
class TestUpdatePortfolio(MultiDBTestCase):
    """
    Tests for PUT /v1/program-review-tool/portfolio endpoint.
    """

    url: str = reverse("program_review_tool.portfolio")

    @tag("views.portfolio.update_portfolio")
    def test_update_portfolio(self) -> None:
        """Success Case: Update a `Portfolio` record."""

    @tag("views.portfolio.update_portfolio_dne")
    def test_update_portfolio_record_dne(self) -> None:
        """Fail Case: Update a `Portfolio` record that
        does not exist."""

    @tag("views.portfolio.update_portfolio_empty_name")
    def test_update_portfolio_empty_name(self) -> None:
        """Fail Case: Update a `Portfolio` record with
        an empty name."""

    @tag("views.portfolio.update_portfolio_duplicate_name")
    def test_update_portfolio_duplicate_name(self) -> None:
        """Fail Case: Update a `Portfolio` record with
        a duplicate name for the given user."""

    @tag("views.portfolio.update_portfolio_empty_programs")
    def test_update_portfolio_empty_programs(self) -> None:
        """Fail Case: Update a `Portfolio` record without supplying
        `Program` ids."""

    @tag("views.portfolio.update_portfolio_programs_dne")
    def test_update_portfolio_programs_dne(self) -> None:
        """Fail Case: Update a `Portfolio` record, supplying
        ids for `Program`s that do not exist."""
