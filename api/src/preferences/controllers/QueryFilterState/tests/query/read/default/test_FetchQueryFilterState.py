"""
Collection of pytests for QueryFilterState's fetch controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "preferences",
    "queryfilterstate",
    "controllers.TestFetchQueryFilterState",
    "preferences.queryfilterstate.fetch",
    "queryfilterstate.fetch.default",
)
class TestFetchQueryFilterState(TestCase):
    """Test suite for QueryFilterState's fetch controller."""

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

    @tag("controllers.queryfilterstate.fetch_query_filter_state")
    def test_fetch_query_filter_state(self) -> None:
        """Success case: Fetch the `QueryFilterState` record for the
        given user."""

    @tag("controllers.queryfilterstate.fetch_query_filter_state_user_dne")
    def test_fetch_query_filter_state_user_dne(self) -> None:
        """Fail Case: Fetch a `QueryFilterState` record with a `User`
        that does not exist."""
