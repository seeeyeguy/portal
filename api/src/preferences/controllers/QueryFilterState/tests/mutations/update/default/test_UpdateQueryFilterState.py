"""
Collection of pytests for QueryFilterState's update controller.
"""

# pylint: disable=line-too-long,wrong-import-order
import pytest
from typing import List

from django.test import tag, TestCase

from portal.models.fixtures import COMMON_FIXTURES
from preferences.controllers.QueryFilterState.QueryFilterState import QueryFilterState
from preferences.controllers.QueryFilterState.tests.mutations.update.default import (
    arguments,
)
from preferences.exceptions import PreferencesError
from preferences.models.QueryFilterState.QueryFilterState import (
    QueryFilterState as QueryFilterStateModel,
)
from preferences.models.QueryFilterState.serializers import QueryFilterStateSerializer


@tag(
    "controllers",
    "preferences",
    "queryfilterstate",
    "controllers.TestUpdateQueryFilterState",
    "preferences.queryfilterstate.update",
    "queryfilterstate.update.default",
)
class TestUpdateQueryFilterState(TestCase):
    """Test suite for QueryFilterState's update controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "preferences/controllers/QueryFilterState/tests/mutations/update/default/fixtures/resources.json",
        "preferences/controllers/QueryFilterState/tests/mutations/update/default/fixtures/requests.json",
        "preferences/controllers/QueryFilterState/tests/mutations/update/default/fixtures/transitions.json",
        "preferences/controllers/QueryFilterState/tests/mutations/update/default/fixtures/dispositions.json",
        "preferences/controllers/QueryFilterState/tests/mutations/update/default/fixtures/queries.json",
        "preferences/controllers/QueryFilterState/tests/mutations/update/default/fixtures/queryfilterstates.json",
    ]

    @tag("controllers.queryfilterstate.update_query_filter_state")
    def test_update_query_filter_state(self) -> None:
        """Success Case: Update a `QueryFilterState` record."""

        query_filter_state = QueryFilterState.update_query_filter_state(
            record_id=arguments.UPDATE_QUERYFILTERSTATE_ID,
            search=arguments.UPDATE_QUERYFILTERSTATE_QUERY_ID,
            functions=arguments.UPDATE_QUERYFILTERSTATE_FUNCTION_IDS,
            employee_levels=arguments.UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS,
            tags=arguments.UPDATE_QUERYFILTERSTATE_TAG_IDS,
            user=arguments.UPDATE_QUERYFILTERSTATE_USER_EMAIL,
        )

        self.assertIsInstance(query_filter_state, QueryFilterStateModel)

        # Serialize `QueryFilterState`.
        serialized_query_filter_state: dict = QueryFilterStateSerializer(
            query_filter_state
        ).data

        # Remove dynamic datetime field before
        # comparison.
        del serialized_query_filter_state["modified"]

        self.assertEqual(
            serialized_query_filter_state, arguments.VALID_QUERYFILTERSTATE_RECORD
        )

    @tag("controllers.queryfilterstate.update_query_filter_state_record_dne")
    def test_update_query_filter_state_record_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` that does not exist."""

        with pytest.raises(PreferencesError):
            _ = QueryFilterState.update_query_filter_state(
                record_id=arguments.UPDATE_QUERYFILTERSTATE_ID_DNE,
                search=arguments.UPDATE_QUERYFILTERSTATE_QUERY_ID,
                functions=arguments.UPDATE_QUERYFILTERSTATE_FUNCTION_IDS,
                employee_levels=arguments.UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS,
                tags=arguments.UPDATE_QUERYFILTERSTATE_TAG_IDS,
                user=arguments.UPDATE_QUERYFILTERSTATE_USER_EMAIL,
            )

    @tag("controllers.queryfilterstate.update_query_filter_state_search_dne")
    def test_update_query_filter_state_search_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` record with a search `Query`
        that does not exist."""

        with pytest.raises(PreferencesError):
            _ = QueryFilterState.update_query_filter_state(
                record_id=arguments.UPDATE_QUERYFILTERSTATE_ID,
                search=arguments.UPDATE_QUERYFILTERSTATE_QUERY_ID_DNE,
                functions=arguments.UPDATE_QUERYFILTERSTATE_FUNCTION_IDS,
                employee_levels=arguments.UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS,
                tags=arguments.UPDATE_QUERYFILTERSTATE_TAG_IDS,
                user=arguments.UPDATE_QUERYFILTERSTATE_USER_EMAIL,
            )

    @tag("controllers.queryfilterstate.update_query_filter_state_function_dne")
    def test_update_query_filter_state_function_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` record with a `Function`
        that does not exist."""

        with pytest.raises(PreferencesError):
            _ = QueryFilterState.update_query_filter_state(
                record_id=arguments.UPDATE_QUERYFILTERSTATE_ID,
                search=arguments.UPDATE_QUERYFILTERSTATE_QUERY_ID,
                functions=arguments.UPDATE_QUERYFILTERSTATE_FUNCTION_IDS_DNE,
                employee_levels=arguments.UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS,
                tags=arguments.UPDATE_QUERYFILTERSTATE_TAG_IDS,
                user=arguments.UPDATE_QUERYFILTERSTATE_USER_EMAIL,
            )

    @tag("controllers.queryfilterstate.update_query_filter_state_employee_level_dne")
    def test_update_query_filter_state_employee_level_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` record with an `EmployeeLevel`
        that does not exist."""

        with pytest.raises(PreferencesError):
            _ = QueryFilterState.update_query_filter_state(
                record_id=arguments.UPDATE_QUERYFILTERSTATE_ID,
                search=arguments.UPDATE_QUERYFILTERSTATE_QUERY_ID,
                functions=arguments.UPDATE_QUERYFILTERSTATE_FUNCTION_IDS,
                employee_levels=arguments.UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS_DNE,
                tags=arguments.UPDATE_QUERYFILTERSTATE_TAG_IDS,
                user=arguments.UPDATE_QUERYFILTERSTATE_USER_EMAIL,
            )

    @tag("controllers.queryfilterstate.update_query_filter_state_tag_dne")
    def test_update_query_filter_state_tag_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` record with a `Tag`
        that does not exist."""

        with pytest.raises(PreferencesError):
            _ = QueryFilterState.update_query_filter_state(
                record_id=arguments.UPDATE_QUERYFILTERSTATE_ID,
                search=arguments.UPDATE_QUERYFILTERSTATE_QUERY_ID,
                functions=arguments.UPDATE_QUERYFILTERSTATE_FUNCTION_IDS,
                employee_levels=arguments.UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS,
                tags=arguments.UPDATE_QUERYFILTERSTATE_TAG_IDS_DNE,
                user=arguments.UPDATE_QUERYFILTERSTATE_USER_EMAIL,
            )

    @tag("controllers.queryfilterstate.update_query_filter_state_user_dne")
    def test_update_query_filter_state_user_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` record using the
        email of a `User` that does not exist."""

        with pytest.raises(PreferencesError):
            _ = QueryFilterState.update_query_filter_state(
                record_id=arguments.UPDATE_QUERYFILTERSTATE_ID,
                search=arguments.UPDATE_QUERYFILTERSTATE_QUERY_ID,
                functions=arguments.UPDATE_QUERYFILTERSTATE_FUNCTION_IDS,
                employee_levels=arguments.UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS,
                tags=arguments.UPDATE_QUERYFILTERSTATE_TAG_IDS,
                user=arguments.UPDATE_QUERYFILTERSTATE_USER_EMAIL_DNE,
            )

    @tag("controllers.queryfilterstate.update_query_filter_state_user_does_not_match")
    def test_update_query_filter_state_user_does_not_match(self) -> None:
        """Fail Case: Update a `QueryFilterState` record using the
        email of a `User` that does not match the record's user email."""

        with pytest.raises(PreferencesError):
            _ = QueryFilterState.update_query_filter_state(
                record_id=arguments.UPDATE_QUERYFILTERSTATE_ID,
                search=arguments.UPDATE_QUERYFILTERSTATE_QUERY_ID,
                functions=arguments.UPDATE_QUERYFILTERSTATE_FUNCTION_IDS,
                employee_levels=arguments.UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS,
                tags=arguments.UPDATE_QUERYFILTERSTATE_TAG_IDS,
                user=arguments.UPDATE_QUERYFILTERSTATE_USER_EMAIL_DOES_NOT_MATCH,
            )
