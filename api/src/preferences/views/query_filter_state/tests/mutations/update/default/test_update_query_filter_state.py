"""Collection of pytests for the QueryFilterState's update view endpoint."""

from typing import List

from django.test import tag, TestCase
from django.urls import reverse

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "preferences",
    "queryfilterstate",
    "views",
    "preferences.queryfilterstate.update",
    "queryfilterstate.update.default",
    "views.TestUpdateQueryFilterState",
)
class TestUpdateQueryFilterState(TestCase):
    """
    Tests for PUT /v1/preferences/query-filter-state endpoint.
    """

    fixtures: List[str] = [*COMMON_FIXTURES]

    url: str = reverse("preferences.query-filter-state")

    @tag("views.queryfilterstate.update_query_filter_state")
    def test_update_query_filter_state(self) -> None:
        """Success Case: Update a `QueryFilterState` record."""

    @tag("views.queryfilterstate.update_query_filter_state_record_dne")
    def test_update_query_filter_state_record_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` that does not exist."""

    @tag("views.queryfilterstate.update_query_filter_state_search_dne")
    def test_update_query_filter_state_search_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` record with a search `Query`
        that does not exist."""

    @tag("views.queryfilterstate.update_query_filter_state_function_dne")
    def test_update_query_filter_state_function_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` record with a `Function`
        that does not exist."""

    @tag("views.queryfilterstate.update_query_filter_state_employee_level_dne")
    def test_update_query_filter_state_employee_level_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` record with an `EmployeeLevel`
        that does not exist."""

    @tag("views.queryfilterstate.update_query_filter_state_tag_dne")
    def test_update_query_filter_state_tag_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` record with a `Tag`
        that does not exist."""
