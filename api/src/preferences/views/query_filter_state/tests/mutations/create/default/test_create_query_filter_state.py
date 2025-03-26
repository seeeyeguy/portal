"""Collection of pytests for the QueryFilterState's create view endpoint."""

from typing import List

from django.contrib.auth.models import User
from django.test import tag
from django.urls import reverse
from rest_framework import status

from preferences.controllers.QueryFilterState.tests.mutations.create.default import (
    arguments,
)

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "preferences",
    "queryfilterstate",
    "views",
    "preferences.queryfilterstate.create",
    "queryfilterstate.create.default",
    "views.TestCreateQueryFilterState",
)
class TestCreateQueryFilterState(MultiDBTestCase):
    """
    Tests for POST /v1/preferences/query-filter-state endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = User.objects.get(email=arguments.CREATE_QUERY_FILTER_STATE_USER)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "preferences/controllers/QueryFilterState/tests/mutations/create/default/fixtures/dispositions.json",
        "preferences/controllers/QueryFilterState/tests/mutations/create/default/fixtures/queries.json",
        "preferences/controllers/QueryFilterState/tests/mutations/create/default/fixtures/requests.json",
        "preferences/controllers/QueryFilterState/tests/mutations/create/default/fixtures/resources.json",
        "preferences/controllers/QueryFilterState/tests/mutations/create/default/fixtures/transitions.json",
    ]

    url: str = reverse("preferences.query-filter-state")

    @tag("views.queryfilterstate.create_query_filter_state")
    def test_create_query_filter_state(self) -> None:
        """Success Case: Create `QueryFilterState` record."""

        body: dict = {
            "search": arguments.CREATE_QUERY_FILTER_STATE_QUERY_ID,
            "functions": arguments.CREATE_QUERY_FILTER_STATE_FUNCTION_IDS,
            "employee_levels": arguments.CREATE_QUERY_FILTER_STATE_EMPLOYEE_LEVEL_IDS,
            "tags": arguments.CREATE_QUERY_FILTER_STATE_TAG_IDS,
        }

        # Make request to create `QueryFilterState`.
        response = self.client.post(self.url, body, content_type="application/json")

        query_filter_state = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(query_filter_state, dict)

        # Remove dynamic primary key and datetime fields before comparison.
        del query_filter_state["id"]
        del query_filter_state["created"]
        del query_filter_state["modified"]

        self.assertEqual(query_filter_state, arguments.VALID_CREATED_QUERY_FILTER_STATE)

    @tag("views.queryfilterstate.create_query_filter_state_search_dne")
    def test_create_query_filter_state_search_dne(self) -> None:
        """Fail Case: Create a `QueryFilterState` record with a search `Query`
        that does not exist."""

        body: dict = {
            "search": arguments.CREATE_QUERY_FILTER_STATE_QUERY_ID_DNE,
            "functions": arguments.CREATE_QUERY_FILTER_STATE_FUNCTION_IDS,
            "employee_levels": arguments.CREATE_QUERY_FILTER_STATE_EMPLOYEE_LEVEL_IDS,
            "tags": arguments.CREATE_QUERY_FILTER_STATE_TAG_IDS,
        }

        # Make request to create `QueryFilterState`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 404.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.queryfilterstate.create_query_filter_state_function_dne")
    def test_create_query_filter_state_function_dne(self) -> None:
        """Fail Case: Create a `QueryFilterState` record with a `Function`
        that does not exist."""

        body: dict = {
            "search": arguments.CREATE_QUERY_FILTER_STATE_QUERY_ID,
            "functions": arguments.CREATE_QUERY_FILTER_STATE_FUNCTION_ID_DNE,
            "employee_levels": arguments.CREATE_QUERY_FILTER_STATE_EMPLOYEE_LEVEL_IDS,
            "tags": arguments.CREATE_QUERY_FILTER_STATE_TAG_IDS,
        }

        # Make request to create `QueryFilterState`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 404.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.queryfilterstate.create_query_filter_state_employee_level_dne")
    def test_create_query_filter_state_employee_level_dne(self) -> None:
        """Fail Case: Create a `QueryFilterState` record with an `EmployeeLevel`
        that does not exist."""

        body: dict = {
            "search": arguments.CREATE_QUERY_FILTER_STATE_QUERY_ID,
            "functions": arguments.CREATE_QUERY_FILTER_STATE_FUNCTION_IDS,
            "employee_levels": arguments.CREATE_QUERY_FILTER_STATE_EMPLOYEE_LEVEL_ID_DNE,
            "tags": arguments.CREATE_QUERY_FILTER_STATE_TAG_IDS,
        }

        # Make request to create `QueryFilterState`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 404.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.queryfilterstate.create_query_filter_state_tag_dne")
    def test_create_query_filter_state_tag_dne(self) -> None:
        """Fail Case: Create a `QueryFilterState` record with a `Tag`
        that does not exist."""

        body: dict = {
            "search": arguments.CREATE_QUERY_FILTER_STATE_QUERY_ID,
            "functions": arguments.CREATE_QUERY_FILTER_STATE_FUNCTION_IDS,
            "employee_levels": arguments.CREATE_QUERY_FILTER_STATE_EMPLOYEE_LEVEL_IDS,
            "tags": arguments.CREATE_QUERY_FILTER_STATE_TAG_ID_DNE,
        }

        # Make request to create `QueryFilterState`.
        response = self.client.post(self.url, body, content_type="application/json")
        # Ensure the response status code is 404.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
