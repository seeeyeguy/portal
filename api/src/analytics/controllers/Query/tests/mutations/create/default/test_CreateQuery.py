"""
Collection of pytests for Query's create controller.
"""

from typing import List

from django.test import tag, TestCase

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "controllers",
    "analytics",
    "query",
    "controllers.TestCreateQuery",
    "analytics.query.create",
    "query.create.default",
)
class TestCreateQuery(TestCase):
    """Test suite for Query's create controller."""

    fixtures: List[str] = [*COMMON_FIXTURES]

    @tag("controllers.query.create_query")
    def test_create_query(self) -> None:
        """Success Case: Create a `Query` record."""

    @tag("controllers.query.create_query_search_term_no_results")
    def test_create_query_search_term_no_results(self) -> None:
        """Success Case: Create a `Query` record with a
        search term that yielded no results."""

    @tag("controllers.query.create_query_user_dne")
    def test_create_query_user_dne(self) -> None:
        """Fail Case: Create a `Query` record with a `User`
        that does not exist."""
