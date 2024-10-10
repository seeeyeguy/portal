"""Collection of pytests for the Query's fetch view endpoint."""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


@tag(
    "analytics",
    "query",
    "views",
    "analytics.query.fetch",
    "query.fetch.default",
    "views.TestFetchQuery",
)
class TestFetchQuery(TestCase):
    """
    Tests for GET /v1/analytics/queries endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/employeelevels/employeelevels.json",
        "portal/models/fixtures/functions/functions.json",
        "portal/models/fixtures/subfunctions/subfunctions.json",
        "portal/models/fixtures/tags/tags.json",
        "portal/models/fixtures/stages/stages.json",
        "portal/models/fixtures/users/users.json",
        "portal/models/fixtures/roles/roles.json",
        "portal/models/fixtures/accesses/accesses.json",
    ]

    url: str = reverse("analytics.query")

    @tag("views.query.fetch_query")
    def test_fetch_query(self) -> None:
        """Success Case: Fetch all `Query` records."""

    @tag("views.query.fetch_query_with_page")
    def test_fetch_query_with_page(self) -> None:
        """Success Case: Fetch page of `Query` records."""

    @tag("views.query.fetch_query_with_limit")
    def test_fetch_query_with_limit(self) -> None:
        """Success Case: Fetch all `Query` records up to limit."""

    @tag("views.query.fetch_query_with_page_and_limit")
    def test_fetch_query_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Query` records up to limit."""

    @tag("views.query.fetch_query_by_id")
    def test_fetch_query_by_id(self) -> None:
        """Success Case: Fetch a `Query` record given an id."""

    @tag("views.query.fetch_query_by_user")
    def test_fetch_query_by_user(self) -> None:
        """Success Case: Fetch `Query` records given a user's email."""

    @tag("views.query.fetch_query_by_user_with_page")
    def test_fetch_query_by_user_with_page(self) -> None:
        """Success Case: Fetch a page of `Query` records given a
        user's email."""

    @tag("views.query.fetch_query_by_user_with_limit")
    def test_fetch_query_by_user_with_limit(self) -> None:
        """Success Case: Fetch `Query` records given a user's email
        up to limit."""

    @tag("views.query.fetch_query_by_user_with_page_and_limit")
    def test_fetch_query_by_user_with_page_and_limit(self) -> None:
        """Success Case: Fetch a page of `Query` records given a
        user's email up to limit."""

    @tag("views.query.fetch_query_by_id_dne")
    def test_fetch_query_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Query` record given an id where record
        does not exist."""

    @tag("views.query.fetch_query_by_user_dne")
    def test_fetch_query_by_user_dne(self) -> None:
        """Fail Case: Fetch a `Query` record given a user's email
        where `User` does not exist."""
