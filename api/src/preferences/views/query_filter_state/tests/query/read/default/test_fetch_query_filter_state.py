"""Collection of pytests for the QueryFilterState's fetch view endpoint."""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse


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

    url: str = reverse("preferences.query-filter-state")

    @tag("views.queryfilterstate.fetch_query_filter_state")
    def test_fetch_query_filter_state(self) -> None:
        """Success case: Fetch the `QueryFilterState` record for the
        given user."""

    @tag("views.queryfilterstate.fetch_query_filter_state_user_dne")
    def test_fetch_query_filter_state_user_dne(self) -> None:
        """Fail Case: Fetch a `QueryFilterState` record with a `User`
        that does not exist."""
