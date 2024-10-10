"""
Collection of pytests for QueryFilterState's create controller.
"""

from typing import List

from django.test import tag, TestCase


@tag(
    "controllers",
    "preferences",
    "queryfilterstate",
    "controllers.TestCreateQueryFilterState",
    "preferences.queryfilterstate.create",
    "queryfilterstate.create.default",
)
class TestCreateQueryFilterState(TestCase):
    """Test suite for QueryFilterState's create controller."""

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

    @tag("controllers.queryfilterstate.create_query_filter_state")
    def test_create_query_filter_state(self) -> None:
        """Success Case: Create `QueryFilterState` record."""

    @tag("controllers.queryfilterstate.create_query_filter_state_user_dne")
    def test_create_query_filter_state_user_dne(self) -> None:
        """Fail Case: Create a `QueryFilterState` record with a `User`
        that does not exist."""

    @tag("controllers.queryfilterstate.create_query_filter_state_search_dne")
    def test_create_query_filter_state_search_dne(self) -> None:
        """Fail Case: Create a `QueryFilterState` record with a search `Query`
        that does not exist."""

    @tag("controllers.queryfilterstate.create_query_filter_state_function_dne")
    def test_create_query_filter_state_function_dne(self) -> None:
        """Fail Case: Create a `QueryFilterState` record with a `Function`
        that does not exist."""

    @tag("controllers.queryfilterstate.create_query_filter_state_employee_level_dne")
    def test_create_query_filter_state_employee_level_dne(self) -> None:
        """Fail Case: Create a `QueryFilterState` record with an `EmployeeLevel`
        that does not exist."""

    @tag("controllers.queryfilterstate.create_query_filter_state_tag_dne")
    def test_create_query_filter_state_tag_dne(self) -> None:
        """Fail Case: Create a `QueryFilterState` record with a `Tag`
        that does not exist."""
