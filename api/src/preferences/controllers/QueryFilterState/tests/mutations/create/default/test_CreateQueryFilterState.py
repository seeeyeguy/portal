"""
Collection of pytests for QueryFilterState's create controller.
"""

import pytest
from typing import List

from django.test import tag

from preferences import exceptions
from preferences.controllers.QueryFilterState.QueryFilterState import QueryFilterState
from preferences.controllers.QueryFilterState.tests.mutations.create.default import (
    arguments,
)
from preferences.models.QueryFilterState import (
    QueryFilterState as QueryFilterStateModel,
    serializers,
)

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "preferences",
    "queryfilterstate",
    "controllers.TestCreateQueryFilterState",
    "preferences.queryfilterstate.create",
    "queryfilterstate.create.default",
)
class TestCreateQueryFilterState(MultiDBTestCase):
    """Test suite for QueryFilterState's create controller."""

    # pylint: disable=line-too-long
    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "preferences/controllers/QueryFilterState/tests/mutations/create/default/fixtures/dispositions.json",
        "preferences/controllers/QueryFilterState/tests/mutations/create/default/fixtures/queries.json",
        "preferences/controllers/QueryFilterState/tests/mutations/create/default/fixtures/requests.json",
        "preferences/controllers/QueryFilterState/tests/mutations/create/default/fixtures/resources.json",
        "preferences/controllers/QueryFilterState/tests/mutations/create/default/fixtures/transitions.json",
    ]

    @tag("controllers.queryfilterstate.create_query_filter_state")
    def test_create_query_filter_state(self) -> None:
        """Success Case: Create `QueryFilterState` record."""

        # Create `QueryFilterState` record.
        query_filter_state = QueryFilterState.create_query_filter_state(
            user=arguments.CREATE_QUERY_FILTER_STATE_USER,
            search=arguments.CREATE_QUERY_FILTER_STATE_QUERY_ID,
            functions=arguments.CREATE_QUERY_FILTER_STATE_FUNCTION_IDS,
            employee_levels=arguments.CREATE_QUERY_FILTER_STATE_EMPLOYEE_LEVEL_IDS,
            tags=arguments.CREATE_QUERY_FILTER_STATE_TAG_IDS,
        )

        self.assertIsInstance(query_filter_state, QueryFilterStateModel)

        # Serialize `QueryFilterState`.
        serialized_query_filter_state = serializers.QueryFilterStateSerializer(
            query_filter_state
        ).data

        # Remove dynamic primary key and datetime fields before comparison.
        del serialized_query_filter_state["id"]
        del serialized_query_filter_state["created"]
        del serialized_query_filter_state["modified"]

        self.assertEqual(
            serialized_query_filter_state, arguments.VALID_CREATED_QUERY_FILTER_STATE
        )

    @tag("controllers.queryfilterstate.create_query_filter_state_user_dne")
    def test_create_query_filter_state_user_dne(self) -> None:
        """Fail Case: Create a `QueryFilterState` record with a `User`
        that does not exist."""

        with pytest.raises(exceptions.PreferencesError):
            _ = QueryFilterState.create_query_filter_state(
                user=arguments.CREATE_QUERY_FILTER_STATE_USER_DNE,
                search=arguments.CREATE_QUERY_FILTER_STATE_QUERY_ID,
                functions=arguments.CREATE_QUERY_FILTER_STATE_FUNCTION_IDS,
                employee_levels=arguments.CREATE_QUERY_FILTER_STATE_EMPLOYEE_LEVEL_IDS,
                tags=arguments.CREATE_QUERY_FILTER_STATE_TAG_IDS,
            )

    @tag("controllers.queryfilterstate.create_query_filter_state_search_dne")
    def test_create_query_filter_state_search_dne(self) -> None:
        """Fail Case: Create a `QueryFilterState` record with a search `Query`
        that does not exist."""

        with pytest.raises(exceptions.PreferencesError):
            _ = QueryFilterState.create_query_filter_state(
                user=arguments.CREATE_QUERY_FILTER_STATE_USER,
                search=arguments.CREATE_QUERY_FILTER_STATE_QUERY_ID_DNE,
                functions=arguments.CREATE_QUERY_FILTER_STATE_FUNCTION_IDS,
                employee_levels=arguments.CREATE_QUERY_FILTER_STATE_EMPLOYEE_LEVEL_IDS,
                tags=arguments.CREATE_QUERY_FILTER_STATE_TAG_IDS,
            )

    @tag("controllers.queryfilterstate.create_query_filter_state_function_dne")
    def test_create_query_filter_state_function_dne(self) -> None:
        """Fail Case: Create a `QueryFilterState` record with a `Function`
        that does not exist."""

        with pytest.raises(exceptions.PreferencesError):
            _ = QueryFilterState.create_query_filter_state(
                user=arguments.CREATE_QUERY_FILTER_STATE_USER,
                search=arguments.CREATE_QUERY_FILTER_STATE_QUERY_ID,
                functions=arguments.CREATE_QUERY_FILTER_STATE_FUNCTION_ID_DNE,
                employee_levels=arguments.CREATE_QUERY_FILTER_STATE_EMPLOYEE_LEVEL_IDS,
                tags=arguments.CREATE_QUERY_FILTER_STATE_TAG_IDS,
            )

    @tag("controllers.queryfilterstate.create_query_filter_state_employee_level_dne")
    def test_create_query_filter_state_employee_level_dne(self) -> None:
        """Fail Case: Create a `QueryFilterState` record with an `EmployeeLevel`
        that does not exist."""

        with pytest.raises(exceptions.PreferencesError):
            _ = QueryFilterState.create_query_filter_state(
                user=arguments.CREATE_QUERY_FILTER_STATE_USER,
                search=arguments.CREATE_QUERY_FILTER_STATE_QUERY_ID,
                functions=arguments.CREATE_QUERY_FILTER_STATE_FUNCTION_IDS,
                employee_levels=arguments.CREATE_QUERY_FILTER_STATE_EMPLOYEE_LEVEL_ID_DNE,
                tags=arguments.CREATE_QUERY_FILTER_STATE_TAG_IDS,
            )

    @tag("controllers.queryfilterstate.create_query_filter_state_tag_dne")
    def test_create_query_filter_state_tag_dne(self) -> None:
        """Fail Case: Create a `QueryFilterState` record with a `Tag`
        that does not exist."""

        with pytest.raises(exceptions.PreferencesError):
            _ = QueryFilterState.create_query_filter_state(
                user=arguments.CREATE_QUERY_FILTER_STATE_USER,
                search=arguments.CREATE_QUERY_FILTER_STATE_QUERY_ID,
                functions=arguments.CREATE_QUERY_FILTER_STATE_FUNCTION_IDS,
                employee_levels=arguments.CREATE_QUERY_FILTER_STATE_EMPLOYEE_LEVEL_IDS,
                tags=arguments.CREATE_QUERY_FILTER_STATE_TAG_ID_DNE,
            )
