"""
Collection of pytests for QueryFilterState's fetch controller.
"""

# pylint: disable=line-too-long,wrong-import-order
import pytest
from typing import List

from django.test import tag, TestCase

from portal.models.fixtures import COMMON_FIXTURES

from preferences.controllers.QueryFilterState.QueryFilterState import QueryFilterState
from preferences.controllers.QueryFilterState.tests.query.read.default import arguments
from preferences.exceptions import PreferencesError
from preferences.models.QueryFilterState.QueryFilterState import (
    QueryFilterState as QueryFilterStateModel,
)
from preferences.models.QueryFilterState.serializers import QueryFilterStateSerializer


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
        *COMMON_FIXTURES,
        "preferences/controllers/QueryFilterState/tests/query/read/default/fixtures/resources.json",
        "preferences/controllers/QueryFilterState/tests/query/read/default/fixtures/requests.json",
        "preferences/controllers/QueryFilterState/tests/query/read/default/fixtures/transitions.json",
        "preferences/controllers/QueryFilterState/tests/query/read/default/fixtures/dispositions.json",
        "preferences/controllers/QueryFilterState/tests/query/read/default/fixtures/queries.json",
        "preferences/controllers/QueryFilterState/tests/query/read/default/fixtures/queryfilterstate.json",
    ]

    @tag("controllers.queryfilterstate.fetch_query_filter_state")
    def test_fetch_query_filter_state(self) -> None:
        """Success case: Fetch the `QueryFilterState` record for the
        given user."""

        query_filter_state = QueryFilterState.fetch_query_filter_state(
            user=arguments.FETCH_QUERYFILTERSTATE_USER_EMAIL
        )

        self.assertIsInstance(query_filter_state, QueryFilterStateModel)

        self.assertEqual(
            QueryFilterStateSerializer(query_filter_state).data,
            arguments.VALID_QUERYFILTERSTATE_RECORD,
        )

    @tag("controllers.queryfilterstate.fetch_query_filter_state_user_dne")
    def test_fetch_query_filter_state_user_dne(self) -> None:
        """Fail Case: Fetch a `QueryFilterState` record with a `User`
        that does not exist."""

        with pytest.raises(PreferencesError):
            _ = QueryFilterState.fetch_query_filter_state(
                user=arguments.FETCH_QUERYFILTERSTATE_USER_EMAIL_DNE
            )
