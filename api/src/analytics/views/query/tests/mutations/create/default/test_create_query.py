"""Collection of pytests for the Query's create view endpoint."""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from analytics.controllers.Query.tests.mutations.create.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "analytics",
    "query",
    "views",
    "analytics.query.create",
    "query.create.default",
    "views.TestCreateQuery",
)
class TestCreateQuery(MultiDBTestCase):
    """
    Tests for POST /v1/analytics/queries endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(
            email__iexact=arguments.CREATE_QUERY_USER_EMAIL
        )
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "analytics/controllers/Query/tests/mutations/create/default/fixtures/resources.json",
        "analytics/controllers/Query/tests/mutations/create/default/fixtures/requests.json",
        "analytics/controllers/Query/tests/mutations/create/default/fixtures/transitions.json",
        "analytics/controllers/Query/tests/mutations/create/default/fixtures/dispositions.json",
    ]

    url: str = reverse("analytics.query")

    @tag("views.query.create_query")
    def test_create_query(self) -> None:
        """Success Case: Create a `Query` record."""

        body: dict = {
            "search_term": arguments.CREATE_QUERY_SEARCH_TERM,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        query = response.json()

        # Check the response status code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        del query["created"]
        del query["id"]

        self.assertEqual(query, arguments.VALID_CREATED_QUERY)

    @tag("views.query.create_query_search_term_no_results")
    def test_create_query_search_term_no_results(self) -> None:
        """Success Case: Create a `Query` record with a
        search term that yielded no results."""

        body: dict = {
            "search_term": arguments.SEARCH_TERM_NO_RESULTS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        query = response.json()

        # Check the response status code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        del query["created"]
        del query["id"]

        self.assertEqual(query, arguments.VALID_NO_RESULTS_QUERY)
