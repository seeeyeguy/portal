"""Collection of pytests for the QueryFilterState's update view endpoint."""

# pylint: disable=line-too-long
from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from preferences.controllers.QueryFilterState.tests.mutations.update.default import (
    arguments,
)

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "preferences",
    "queryfilterstate",
    "views",
    "preferences.queryfilterstate.update",
    "queryfilterstate.update.default",
    "views.TestUpdateQueryFilterState",
)
class TestUpdateQueryFilterState(MultiDBTestCase):
    """
    Tests for PUT /v1/preferences/query-filter-state endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(
            email__iexact=arguments.UPDATE_QUERYFILTERSTATE_USER_EMAIL
        )
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "preferences/controllers/QueryFilterState/tests/mutations/update/default/fixtures/resources.json",
        "preferences/controllers/QueryFilterState/tests/mutations/update/default/fixtures/requests.json",
        "preferences/controllers/QueryFilterState/tests/mutations/update/default/fixtures/transitions.json",
        "preferences/controllers/QueryFilterState/tests/mutations/update/default/fixtures/dispositions.json",
        "preferences/controllers/QueryFilterState/tests/mutations/update/default/fixtures/queries.json",
        "preferences/controllers/QueryFilterState/tests/mutations/update/default/fixtures/queryfilterstates.json",
    ]

    url: str = reverse("preferences.query-filter-state")

    @tag("views.queryfilterstate.update_query_filter_state")
    def test_update_query_filter_state(self) -> None:
        """Success Case: Update a `QueryFilterState` record."""

        body: dict = {
            "search": arguments.UPDATE_QUERYFILTERSTATE_QUERY_ID,
            "functions": arguments.UPDATE_QUERYFILTERSTATE_FUNCTION_IDS,
            "employee_levels": arguments.UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS,
            "tags": arguments.UPDATE_QUERYFILTERSTATE_TAG_IDS,
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_QUERYFILTERSTATE_ID}"

        response = self.client.put(request_url, body, content_type="application/json")

        query_filter_state = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(query_filter_state, dict)

        # Remove dynamic datetime field before
        # comparison.
        del query_filter_state["modified"]

        self.assertEqual(query_filter_state, arguments.VALID_QUERYFILTERSTATE_RECORD)

    @tag("views.queryfilterstate.update_query_filter_state_record_dne")
    def test_update_query_filter_state_record_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` that does not exist."""

        body: dict = {
            "search": arguments.UPDATE_QUERYFILTERSTATE_QUERY_ID,
            "functions": arguments.UPDATE_QUERYFILTERSTATE_FUNCTION_IDS,
            "employee_levels": arguments.UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS,
            "tags": arguments.UPDATE_QUERYFILTERSTATE_TAG_IDS,
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_QUERYFILTERSTATE_ID_DNE}"

        response = self.client.put(request_url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.queryfilterstate.update_query_filter_state_search_dne")
    def test_update_query_filter_state_search_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` record with a search `Query`
        that does not exist."""

        body: dict = {
            "search": arguments.UPDATE_QUERYFILTERSTATE_QUERY_ID_DNE,
            "functions": arguments.UPDATE_QUERYFILTERSTATE_FUNCTION_IDS,
            "employee_levels": arguments.UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS,
            "tags": arguments.UPDATE_QUERYFILTERSTATE_TAG_IDS,
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_QUERYFILTERSTATE_ID}"

        response = self.client.put(request_url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.queryfilterstate.update_query_filter_state_function_dne")
    def test_update_query_filter_state_function_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` record with a `Function`
        that does not exist."""

        body: dict = {
            "search": arguments.UPDATE_QUERYFILTERSTATE_QUERY_ID,
            "functions": arguments.UPDATE_QUERYFILTERSTATE_FUNCTION_IDS_DNE,
            "employee_levels": arguments.UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS,
            "tags": arguments.UPDATE_QUERYFILTERSTATE_TAG_IDS,
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_QUERYFILTERSTATE_ID}"

        response = self.client.put(request_url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.queryfilterstate.update_query_filter_state_employee_level_dne")
    def test_update_query_filter_state_employee_level_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` record with an `EmployeeLevel`
        that does not exist."""

        body: dict = {
            "search": arguments.UPDATE_QUERYFILTERSTATE_QUERY_ID,
            "functions": arguments.UPDATE_QUERYFILTERSTATE_FUNCTION_IDS,
            "employee_levels": arguments.UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS_DNE,
            "tags": arguments.UPDATE_QUERYFILTERSTATE_TAG_IDS,
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_QUERYFILTERSTATE_ID}"

        response = self.client.put(request_url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.queryfilterstate.update_query_filter_state_tag_dne")
    def test_update_query_filter_state_tag_dne(self) -> None:
        """Fail Case: Update a `QueryFilterState` record with a `Tag`
        that does not exist."""

        body: dict = {
            "search": arguments.UPDATE_QUERYFILTERSTATE_QUERY_ID,
            "functions": arguments.UPDATE_QUERYFILTERSTATE_FUNCTION_IDS,
            "employee_levels": arguments.UPDATE_QUERYFILTERSTATE_EMPLOYEELEVEL_IDS,
            "tags": arguments.UPDATE_QUERYFILTERSTATE_TAG_IDS_DNE,
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_QUERYFILTERSTATE_ID}"

        response = self.client.put(request_url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
