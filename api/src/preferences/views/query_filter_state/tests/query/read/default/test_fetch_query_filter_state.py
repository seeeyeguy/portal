"""Collection of pytests for the QueryFilterState's fetch view endpoint."""

# pylint: disable=line-too-long
from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from preferences.controllers.QueryFilterState.tests.query.read.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "preferences",
    "queryfilterstate",
    "views",
    "preferences.queryfilterstate.fetch",
    "queryfilterstate.fetch.default",
    "views.TestFetchQueryFilterState",
)
class TestFetchQueryFilterState(MultiDBTestCase):
    """
    Tests for GET /v1/preferences/query-filter-state endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(
            email__iexact=arguments.FETCH_QUERYFILTERSTATE_USER_EMAIL
        )
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "preferences/controllers/QueryFilterState/tests/query/read/default/fixtures/resources.json",
        "preferences/controllers/QueryFilterState/tests/query/read/default/fixtures/requests.json",
        "preferences/controllers/QueryFilterState/tests/query/read/default/fixtures/transitions.json",
        "preferences/controllers/QueryFilterState/tests/query/read/default/fixtures/dispositions.json",
        "preferences/controllers/QueryFilterState/tests/query/read/default/fixtures/queries.json",
        "preferences/controllers/QueryFilterState/tests/query/read/default/fixtures/queryfilterstate.json",
    ]

    url: str = reverse("preferences.query-filter-state")

    @tag("views.queryfilterstate.fetch_query_filter_state")
    def test_fetch_query_filter_state(self) -> None:
        """Success case: Fetch the `QueryFilterState` record for the
        given user."""

        request_url: str = (
            f"{self.url}?user={arguments.FETCH_QUERYFILTERSTATE_USER_EMAIL}"
        )

        response = self.client.get(
            request_url, headers={"content-type": "application/json"}
        )

        query_filter_state = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(query_filter_state, dict)
        self.assertEqual(query_filter_state, arguments.VALID_QUERYFILTERSTATE_RECORD)

    @tag("views.queryfilterstate.fetch_query_filter_state_user_dne")
    def test_fetch_query_filter_state_user_dne(self) -> None:
        """Fail Case: Fetch a `QueryFilterState` record with a `User`
        that does not exist."""

        request_url: str = (
            f"{self.url}?user={arguments.FETCH_QUERYFILTERSTATE_USER_EMAIL_DNE}"
        )

        response = self.client.get(
            request_url, headers={"content-type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.queryfilterstate.fetch_query_filter_state_dne")
    def test_fetch_query_filter_state_dne(self) -> None:
        """Fail Case: Fetch a `QueryFilterState` record with a `User`
        that does not have an associated `QueryFilterState`."""

        request_url: str = f"{self.url}?user={arguments.FETCH_QUERYFILTERSTATE_QUERYFILTERSTATE_DNE_USER_EMAIL}"

        response = self.client.get(
            request_url, headers={"content-type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
