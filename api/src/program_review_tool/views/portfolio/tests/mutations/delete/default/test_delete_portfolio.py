"""
Collection of pytests for Portfolio's delete view endpoint.
"""

from django.test import tag
from django.urls import reverse

from manager.utils.tests import MultiDBTestCase


@tag(
    "portfolio",
    "program_review_tool",
    "views",
    "portfolio.delete.default",
    "program_review_tool.portfolio.delete",
    "views.TestDeletePortfolio",
)
class TestDeletePortfolio(MultiDBTestCase):
    """
    Tests for DELETE /v1/program-review-tool/portfolio endpoint.
    """

    url: str = reverse("program_review_tool.portfolio")

    @tag("views.portfolio.delete_portfolio")
    def test_delete_portfolio(self) -> None:
        """Success Case: Delete a `Portfolio` record with given id."""
