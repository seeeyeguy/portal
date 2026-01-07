"""Collection of pytests for the Query's fetch view endpoint."""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from analytics.controllers.Query.tests.query.read.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "analytics",
    "query",
    "views",
    "analytics.query.fetch",
    "query.fetch.default",
    "views.TestFetchQuery",
)
class TestFetchQuery(MultiDBTestCase):
    """
    Tests for GET /v1/analytics/queries endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(email=arguments.FETCH_QUERY_BY_USER)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "analytics/controllers/Query/tests/query/read/default/fixtures/resources.json",
        "analytics/controllers/Query/tests/query/read/default/fixtures/pointofcontacts.json",
        "analytics/controllers/Query/tests/query/read/default/fixtures/requests.json",
        "analytics/controllers/Query/tests/query/read/default/fixtures/transitions.json",
        "analytics/controllers/Query/tests/query/read/default/fixtures/dispositions.json",
        "analytics/controllers/Query/tests/query/read/default/fixtures/queries.json",
    ]

    url: str = reverse("analytics.query")

    @tag("views.query.fetch_query")
    def test_fetch_query(self) -> None:
        """Success Case: Fetch all `Query` records."""

        response = self.client.get(
            self.url, headers={"content-type": "application/json"}
        )

        queries = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(queries, list)

        self.assertEqual(len(queries), arguments.FETCH_QUERY_RECORD_COUNT)

        for query in queries:
            query_id: int = query["id"]

            self.assertIsInstance(query, dict)

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

            self.assertEqual(
                query,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("views.query.fetch_query_with_page")
    def test_fetch_query_with_page(self) -> None:
        """Success Case: Fetch page of `Query` records."""

        query_params: dict = {
            "page": arguments.FETCH_QUERY_WITH_PAGE,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        queries = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(queries, list)

        self.assertEqual(len(queries), arguments.FETCH_QUERY_WITH_PAGE_RECORD_COUNT)

        for query in queries:
            query_id: int = query["id"]

            self.assertIsInstance(query, dict)

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

            self.assertEqual(
                query,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("views.query.fetch_query_by_resource_id_with_page")
    def test_fetch_query_by_resource_id_with_page(self) -> None:
        """Success Case: Fetch page of `Query` records filtered by `Resource` id."""

        query_params: dict = {
            "resource_id": arguments.FETCH_QUERY_BY_RESOURCE_ID,
            "page": arguments.FETCH_QUERY_WITH_PAGE,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        queries = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(queries, list)

        self.assertEqual(len(queries), arguments.FETCH_QUERY_BY_RESOURCE_RECORD_COUNT)

        for query in queries:
            query_id: int = query["id"]

            self.assertIsInstance(query, dict)

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

            self.assertEqual(
                query,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("views.query.fetch_query_with_limit")
    def test_fetch_query_with_limit(self) -> None:
        """Success Case: Fetch all `Query` records up to limit."""

        query_params: dict = {
            "limit": arguments.FETCH_QUERY_WITH_LIMIT,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        queries = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(queries, list)

        self.assertEqual(len(queries), arguments.FETCH_QUERY_WITH_LIMIT_RECORD_COUNT)

        for query in queries:
            query_id: int = query["id"]

            self.assertIsInstance(query, dict)

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

            self.assertEqual(
                query,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("views.query.fetch_query_by_resource_id_with_limit")
    def test_fetch_query_by_resource_id_with_limit(self) -> None:
        """Success Case: Fetch `Query` records filtered by `Resource` id up to limit."""

        query_params: dict = {
            "resource_id": arguments.FETCH_QUERY_BY_RESOURCE_ID,
            "limit": arguments.FETCH_QUERY_WITH_LIMIT,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        queries = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(queries, list)

        self.assertEqual(len(queries), arguments.FETCH_QUERY_BY_RESOURCE_RECORD_COUNT)

        for query in queries:
            query_id: int = query["id"]

            self.assertIsInstance(query, dict)

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

            self.assertEqual(
                query,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("views.query.fetch_query_with_page_and_limit")
    def test_fetch_query_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Query` records up to limit."""

        query_params: dict = {
            "limit": arguments.FETCH_QUERY_WITH_LIMIT,
            "page": arguments.FETCH_QUERY_WITH_PAGE,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        queries = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(queries, list)

        self.assertEqual(
            len(queries), arguments.FETCH_QUERY_WITH_PAGE_AND_LIMIT_RECORD_COUNT
        )

        for query in queries:
            query_id: int = query["id"]

            self.assertIsInstance(query, dict)

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

            self.assertEqual(
                query,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("views.query.fetch_query_by_resource_id_with_page_and_limit")
    def test_fetch_query_by_resource_id_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Query` records filtered by `Resource` id up to limit."""

        query_params: dict = {
            "resource_id": arguments.FETCH_QUERY_BY_RESOURCE_ID,
            "limit": arguments.FETCH_QUERY_WITH_LIMIT,
            "page": arguments.FETCH_QUERY_WITH_PAGE,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        queries = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(queries, list)

        self.assertEqual(len(queries), arguments.FETCH_QUERY_BY_RESOURCE_RECORD_COUNT)

        for query in queries:
            query_id: int = query["id"]

            self.assertIsInstance(query, dict)

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

            self.assertEqual(
                query,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("views.query.fetch_query_by_id")
    def test_fetch_query_by_id(self) -> None:
        """Success Case: Fetch a `Query` record given an id."""

        query_params: dict = {
            "id": arguments.FETCH_QUERY_BY_ID,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        query = response.json()

        self.assertIsInstance(query, dict)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        query_id: int = query["id"]

        self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

        self.assertEqual(
            query,
            arguments.VALID_QUERY_RECORDS[query_id],
        )

    @tag("views.query.fetch_query_by_resource_id")
    def test_fetch_query_by_resource_id(self) -> None:
        """Success Case: Fetch `Query` records filtered by `Resource` id."""

        query_params: dict = {
            "resource_id": arguments.FETCH_QUERY_BY_RESOURCE_ID,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        query = response.json()

        self.assertIsInstance(query, list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        query_id: int = query[0]["id"]

        self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

        self.assertEqual(
            query[0],
            arguments.VALID_QUERY_RECORDS[query_id],
        )

    @tag("views.query.fetch_query_by_user")
    def test_fetch_query_by_user(self) -> None:
        """Success Case: Fetch `Query` records given a username."""

        query_params: dict = {
            "user": arguments.FETCH_QUERY_BY_USER,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        queries = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(queries, list)

        self.assertEqual(len(queries), arguments.FETCH_QUERY_BY_USER_RECORD_COUNT)

        for query in queries:
            query_id: int = query["id"]

            self.assertIsInstance(query, dict)

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

            self.assertEqual(
                query,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("views.query.fetch_query_by_resource_id_for_user")
    def test_fetch_query_by_resource_id_for_user(self) -> None:
        """Success Case: Fetch `Query` records filtered by `Resource` id and a username."""

        query_params: dict = {
            "resource_id": arguments.FETCH_QUERY_BY_RESOURCE_ID,
            "user": arguments.FETCH_QUERY_BY_USER,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        queries = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(queries, list)

        self.assertEqual(len(queries), arguments.FETCH_QUERY_BY_RESOURCE_RECORD_COUNT)

        for query in queries:
            query_id: int = query["id"]

            self.assertIsInstance(query, dict)

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

            self.assertEqual(
                query,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("views.query.fetch_query_by_user_with_page")
    def test_fetch_query_by_user_with_page(self) -> None:
        """Success Case: Fetch a page of `Query` records given a
        username."""

        query_params: dict = {
            "user": arguments.FETCH_QUERY_BY_USER,
            "page": arguments.FETCH_QUERY_WITH_PAGE,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        queries = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(queries, list)

        self.assertEqual(
            len(queries), arguments.FETCH_QUERY_BY_USER_WITH_PAGE_RECORD_COUNT
        )

        for query in queries:
            query_id: int = query["id"]

            self.assertIsInstance(query, dict)

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

            self.assertEqual(
                query,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("views.query.fetch_query_by_resource_id_for_user_with_page")
    def test_fetch_query_by_resource_id_for_user_with_page(self) -> None:
        """Success Case: Fetch page of `Query` records filtered by `Resource` id and a username."""

        query_params: dict = {
            "resource_id": arguments.FETCH_QUERY_BY_RESOURCE_ID,
            "user": arguments.FETCH_QUERY_BY_USER,
            "page": arguments.FETCH_QUERY_WITH_PAGE,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        queries = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(queries, list)

        self.assertEqual(len(queries), arguments.FETCH_QUERY_BY_RESOURCE_RECORD_COUNT)

        for query in queries:
            query_id: int = query["id"]

            self.assertIsInstance(query, dict)

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

            self.assertEqual(
                query,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("views.query.fetch_query_by_user_with_limit")
    def test_fetch_query_by_user_with_limit(self) -> None:
        """Success Case: Fetch `Query` records given a username
        up to limit."""

        query_params: dict = {
            "user": arguments.FETCH_QUERY_BY_USER,
            "limit": arguments.FETCH_QUERY_WITH_LIMIT,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        queries = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(queries, list)

        self.assertEqual(
            len(queries), arguments.FETCH_QUERY_BY_USER_WITH_LIMIT_RECORD_COUNT
        )

        for query in queries:
            query_id: int = query["id"]

            self.assertIsInstance(query, dict)

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

            self.assertEqual(
                query,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("views.query.fetch_query_by_resource_id_for_user_with_limit")
    def test_fetch_query_by_resource_id_for_user_with_limit(self) -> None:
        """Success Case: Fetch `Query` records filtered by `Resource` id and a username up to limit."""

        query_params: dict = {
            "resource_id": arguments.FETCH_QUERY_BY_RESOURCE_ID,
            "user": arguments.FETCH_QUERY_BY_USER,
            "limit": arguments.FETCH_QUERY_WITH_LIMIT,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        queries = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(queries, list)

        self.assertEqual(
            len(queries), arguments.FETCH_QUERY_BY_USER_WITH_LIMIT_RECORD_COUNT
        )

        for query in queries:
            query_id: int = query["id"]

            self.assertIsInstance(query, dict)

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

            self.assertEqual(
                query,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("views.query.fetch_query_by_user_with_page_and_limit")
    def test_fetch_query_by_user_with_page_and_limit(self) -> None:
        """Success Case: Fetch a page of `Query` records given a
        username up to limit."""

        query_params: dict = {
            "user": arguments.FETCH_QUERY_BY_USER,
            "page": arguments.FETCH_QUERY_WITH_PAGE,
            "limit": arguments.FETCH_QUERY_WITH_LIMIT,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        queries = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(queries, list)

        self.assertEqual(
            len(queries),
            arguments.FETCH_QUERY_BY_USER_WITH_PAGE_AND_LIMIT_RECORD_COUNT,
        )

        for query in queries:
            query_id: int = query["id"]

            self.assertIsInstance(query, dict)

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

            self.assertEqual(
                query,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("views.query.fetch_query_by_resource_id_for_user_with_page_and_limit")
    def test_fetch_query_by_resource_id_for_user_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Query` records filtered by `Resource` id and a username up to limit."""

        query_params: dict = {
            "resource_id": arguments.FETCH_QUERY_BY_RESOURCE_ID,
            "user": arguments.FETCH_QUERY_BY_USER,
            "page": arguments.FETCH_QUERY_WITH_PAGE,
            "limit": arguments.FETCH_QUERY_WITH_LIMIT,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        queries = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(queries, list)

        self.assertEqual(
            len(queries),
            arguments.FETCH_QUERY_BY_RESOURCE_RECORD_COUNT,
        )

        for query in queries:
            query_id: int = query["id"]

            self.assertIsInstance(query, dict)

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)

            self.assertEqual(
                query,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("views.query.fetch_query_with_search_term_no_match")
    def test_fetch_query_with_search_term_no_match(self) -> None:
        """Success Case: `search_term` returns no matching records."""

        query_params: dict = {
            "search_term": "nonexistent term",
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    @tag("views.query.fetch_query_by_id_dne")
    def test_fetch_query_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Query` record given an id where record
        does not exist."""

        query_params: dict = {
            "id": arguments.FETCH_QUERY_BY_ID_DNE,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.query.fetch_query_by_resource_id_dne")
    def test_fetch_query_by_resource_id_dne(self) -> None:
        """Fail Case: Fetch `Query` records given a `Resource` id where the `Resource` does not exist."""

        query_params: dict = {
            "resource_id": arguments.FETCH_QUERY_BY_RESOURCE_ID_DNE,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.query.fetch_query_by_user_dne")
    def test_fetch_query_by_user_dne(self) -> None:
        """Fail Case: Fetch a `Query` record given a username
        where `User` does not exist."""

        query_params: dict = {
            "user": arguments.FETCH_QUERY_BY_USER_DNE,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.query.fetch_query_by_id_with_page")
    def test_fetch_query_by_id_with_page(self) -> None:
        """Fail Case: Fetch a `Query` record given an id where
        a page is also supplied in the parameters."""

        query_params: dict = {
            "id": arguments.FETCH_QUERY_BY_ID,
            "page": arguments.FETCH_QUERY_WITH_PAGE,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.query.fetch_query_by_id_with_limit")
    def test_fetch_query_by_id_with_limit(self) -> None:
        """Fail Case: Fetch a `Query` record given an id where
        a limit is also supplied in the parameters."""

        query_params: dict = {
            "id": arguments.FETCH_QUERY_BY_ID,
            "limit": arguments.FETCH_QUERY_WITH_LIMIT,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.query.fetch_query_by_id_with_page_and_limit")
    def test_fetch_query_by_id_with_page_and_limit(self) -> None:
        """Fail Case: Fetch a `Query` record given an id where
        a page and limit is also supplied in the parameters."""

        query_params: dict = {
            "id": arguments.FETCH_QUERY_BY_ID,
            "page": arguments.FETCH_QUERY_WITH_PAGE,
            "limit": arguments.FETCH_QUERY_WITH_LIMIT,
        }

        response = self.client.get(
            self.url, query_params, headers={"content-type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
