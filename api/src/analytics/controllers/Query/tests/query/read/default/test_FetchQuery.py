"""
Collection of pytests for Query's fetch controller.
"""

from typing import List

from django.test import tag, TestCase

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "controllers",
    "analytics",
    "query",
    "controllers.TestFetchQuery",
    "analytics.query.fetch",
    "query.fetch.default",
)
class TestFetchQuery(TestCase):
    """Test suite for Query's fetch controller."""

    fixtures: List[str] = [*COMMON_FIXTURES]

    @tag("controllers.query.fetch_query")
    def test_fetch_query(self) -> None:
        """Success Case: Fetch all `Query` records."""

    @tag("controllers.query.fetch_query_with_page")
    def test_fetch_query_with_page(self) -> None:
        """Success Case: Fetch page of `Query` records."""

    @tag("controllers.query.fetch_query_with_limit")
    def test_fetch_query_with_limit(self) -> None:
        """Success Case: Fetch all `Query` records up to limit."""

    @tag("controllers.query.fetch_query_with_page_and_limit")
    def test_fetch_query_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Query` records up to limit."""

    @tag("controllers.query.fetch_query_by_id")
    def test_fetch_query_by_id(self) -> None:
        """Success Case: Fetch a `Query` record given an id."""

    @tag("controllers.query.fetch_query_by_user")
    def test_fetch_query_by_user(self) -> None:
        """Success Case: Fetch `Query` records given a user's email."""

    @tag("controllers.query.fetch_query_by_user_with_page")
    def test_fetch_query_by_user_with_page(self) -> None:
        """Success Case: Fetch a page of `Query` records given a
        user's email."""

    @tag("controllers.query.fetch_query_by_user_with_limit")
    def test_fetch_query_by_user_with_limit(self) -> None:
        """Success Case: Fetch `Query` records given a user's email
        up to limit."""

    @tag("controllers.query.fetch_query_by_user_with_page_and_limit")
    def test_fetch_query_by_user_with_page_and_limit(self) -> None:
        """Success Case: Fetch a page of `Query` records given a
        user's email up to limit."""

    @tag("controllers.query.fetch_query_by_id_dne")
    def test_fetch_query_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Query` record given an id where record
        does not exist."""

    @tag("controllers.query.fetch_query_by_user_dne")
    def test_fetch_query_by_user_dne(self) -> None:
        """Fail Case: Fetch a `Query` record given a user's email
        where `User` does not exist."""
