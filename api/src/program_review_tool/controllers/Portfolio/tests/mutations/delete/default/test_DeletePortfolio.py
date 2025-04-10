"""
Collection of pytests for Portfolio's delete controller.
"""

from django.test import tag

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

    @tag("controllers.portfolio.delete_portfolio")
    def test_delete_portfolio(self) -> None:
        """Success Case: Delete `Portfolio` record with the given id."""
