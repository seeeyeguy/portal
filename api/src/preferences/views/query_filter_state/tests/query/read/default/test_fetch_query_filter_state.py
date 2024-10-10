"""Collection of pytests for the QueryFilterState's fetch view endpoint."""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "preferences",
    "queryfilterstate",
    "views",
    "preferences.queryfilterstate.fetch",
    "queryfilterstate.fetch.default",
    "views.TestFetchQueryFilterState",
)
class TestFetchQueryFilterState(TestCase):
    """
    Tests for GET /v1/preferences/query-filter-state endpoint.
    """

    fixtures: List[str] = [*COMMON_FIXTURES]

    url: str = reverse("preferences.query-filter-state")

    @tag("views.queryfilterstate.fetch_query_filter_state")
    def test_fetch_query_filter_state(self) -> None:
        """Success case: Fetch the `QueryFilterState` record for the
        given user."""

    @tag("views.queryfilterstate.fetch_query_filter_state_user_dne")
    def test_fetch_query_filter_state_user_dne(self) -> None:
        """Fail Case: Fetch a `QueryFilterState` record with a `User`
        that does not exist."""
