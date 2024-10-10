"""Collection of pytests for the Query's create view endpoint."""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "analytics",
    "query",
    "views",
    "analytics.query.create",
    "query.create.default",
    "views.TestCreateQuery",
)
class TestCreateQuery(TestCase):
    """
    Tests for POST /v1/analytics/queries endpoint.
    """

    fixtures: List[str] = [*COMMON_FIXTURES]

    url: str = reverse("analytics.query")

    @tag("views.query.create_query")
    def test_create_query(self) -> None:
        """Success Case: Create a `Query` record."""

    @tag("views.query.create_query_search_term_no_results")
    def test_create_query_search_term_no_results(self) -> None:
        """Success Case: Create a `Query` record with a
        search term that yielded no results."""

    @tag("views.query.create_query_user_dne")
    def test_create_query_user_dne(self) -> None:
        """Fail Case: Create a `Query` record with a `User`
        that does not exist."""
