"""
Collection of pytests for Query's fetch controller.
"""

import pytest
from typing import List

from django.db.models import QuerySet
from django.test import tag

from analytics.controllers.Query.Query import Query
from analytics.controllers.Query.tests.query.read.default import arguments
from analytics.exceptions import AnalyticsError
from analytics.models.Query.Query import (
    Query as QueryModel,
)
from analytics.models.Query.serializers import QuerySerializer

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "analytics",
    "query",
    "controllers.TestFetchQuery",
    "analytics.query.fetch",
    "query.fetch.default",
)
class TestFetchQuery(MultiDBTestCase):
    """Test suite for Query's fetch controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "analytics/controllers/Query/tests/query/read/default/fixtures/resources.json",
        "analytics/controllers/Query/tests/query/read/default/fixtures/requests.json",
        "analytics/controllers/Query/tests/query/read/default/fixtures/transitions.json",
        "analytics/controllers/Query/tests/query/read/default/fixtures/dispositions.json",
        "analytics/controllers/Query/tests/query/read/default/fixtures/queries.json",
    ]

    @tag("controllers.query.fetch_query")
    def test_fetch_query(self) -> None:
        """Success Case: Fetch all `Query` records."""

        queries = Query.fetch_query()

        self.assertIsInstance(queries, QuerySet[QueryModel])
        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            self.assertIsInstance(query, QueryModel)

            query_id: int = query.id

            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_with_page")
    def test_fetch_query_with_page(self) -> None:
        """Success Case: Fetch page of `Query` records."""

        queries = Query.fetch_query(page=arguments.FETCH_QUERY_WITH_PAGE)

        self.assertIsInstance(queries, QuerySet[QueryModel])

        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_WITH_PAGE_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            query_id: int = query.id

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)
            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_by_resource_id_with_page")
    def test_fetch_query_by_resource_id_with_page(self) -> None:
        """Success Case: Fetch page of `Query` records filtered by `Resource` id."""

        queries = Query.fetch_query(
            resource_id=arguments.FETCH_QUERY_BY_RESOURCE_ID,
            page=arguments.FETCH_QUERY_WITH_PAGE,
        )

        self.assertIsInstance(queries, QuerySet[QueryModel])

        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_BY_RESOURCE_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            query_id: int = query.id

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)
            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_with_limit")
    def test_fetch_query_with_limit(self) -> None:
        """Success Case: Fetch all `Query` records up to limit."""

        queries = Query.fetch_query(limit=arguments.FETCH_QUERY_WITH_LIMIT)

        self.assertIsInstance(queries, QuerySet[QueryModel])

        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_WITH_LIMIT_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            query_id: int = query.id

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)
            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_by_resource_id_with_limit")
    def test_fetch_query_by_resource_id_with_limit(self) -> None:
        """Success Case: Fetch `Query` records filtered by `Resource` id up to limit."""

        queries = Query.fetch_query(
            resource_id=arguments.FETCH_QUERY_BY_RESOURCE_ID,
            limit=arguments.FETCH_QUERY_WITH_LIMIT,
        )

        self.assertIsInstance(queries, QuerySet[QueryModel])

        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_BY_RESOURCE_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            query_id: int = query.id

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)
            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_with_page_and_limit")
    def test_fetch_query_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Query` records up to limit."""

        queries = Query.fetch_query(
            page=arguments.FETCH_QUERY_WITH_PAGE, limit=arguments.FETCH_QUERY_WITH_LIMIT
        )

        self.assertIsInstance(queries, QuerySet[QueryModel])

        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_WITH_PAGE_AND_LIMIT_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            query_id: int = query.id

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)
            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_by_resource_id_with_page_and_limit")
    def test_fetch_query_by_resource_id_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Query` records filtered by `Resource` id up to limit."""

        queries = Query.fetch_query(
            resource_id=arguments.FETCH_QUERY_BY_RESOURCE_ID,
            page=arguments.FETCH_QUERY_WITH_PAGE,
            limit=arguments.FETCH_QUERY_WITH_LIMIT,
        )

        self.assertIsInstance(queries, QuerySet[QueryModel])

        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_BY_RESOURCE_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            query_id: int = query.id

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)
            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_by_id")
    def test_fetch_query_by_id(self) -> None:
        """Success Case: Fetch a `Query` record given an id."""

        query = Query.fetch_query(
            record_id=arguments.FETCH_QUERY_BY_ID,
        )

        self.assertIsInstance(query, QueryModel)

        query_id: int = query.id  # type: ignore[union-attr]

        self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)
        self.assertEqual(
            QuerySerializer(query).data,
            arguments.VALID_QUERY_RECORDS[query_id],
        )

    @tag("controllers.query.fetch_query_by_resource_id")
    def test_fetch_query_by_resource_id(self) -> None:
        """Success Case: Fetch `Query` records filtered by `Resource` id."""

        queries = Query.fetch_query(resource_id=arguments.FETCH_QUERY_BY_RESOURCE_ID)

        self.assertIsInstance(queries, QuerySet[QueryModel])
        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_BY_RESOURCE_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            self.assertIsInstance(query, QueryModel)

            query_id: int = query.id

            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_by_user")
    def test_fetch_query_by_user(self) -> None:
        """Success Case: Fetch `Query` records given a user's email."""

        queries = Query.fetch_query(user=arguments.FETCH_QUERY_BY_USER)

        self.assertIsInstance(queries, QuerySet[QueryModel])

        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_BY_USER_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            query_id: int = query.id

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)
            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_by_resource_id_for_user")
    def test_fetch_query_by_resource_id_for_user(self) -> None:
        """Success Case: Fetch `Query` records filtered by `Resource` id and a user's email."""

        queries = Query.fetch_query(
            resource_id=arguments.FETCH_QUERY_BY_RESOURCE_ID,
            user=arguments.FETCH_QUERY_BY_USER,
        )

        self.assertIsInstance(queries, QuerySet[QueryModel])

        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_BY_RESOURCE_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            query_id: int = query.id

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)
            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_by_user_with_page")
    def test_fetch_query_by_user_with_page(self) -> None:
        """Success Case: Fetch a page of `Query` records given a
        user's email."""

        queries = Query.fetch_query(
            user=arguments.FETCH_QUERY_BY_USER, page=arguments.FETCH_QUERY_WITH_PAGE
        )

        self.assertIsInstance(queries, QuerySet[QueryModel])

        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_BY_USER_WITH_PAGE_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            query_id: int = query.id

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)
            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_by_resource_id_for_user_with_page")
    def test_fetch_query_by_resource_id_for_user_with_page(self) -> None:
        """Success Case: Fetch page of `Query` records filtered by `Resource` id and a user's email."""

        queries = Query.fetch_query(
            resource_id=arguments.FETCH_QUERY_BY_RESOURCE_ID,
            user=arguments.FETCH_QUERY_BY_USER,
            page=arguments.FETCH_QUERY_WITH_PAGE,
        )

        self.assertIsInstance(queries, QuerySet[QueryModel])

        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_BY_RESOURCE_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            query_id: int = query.id

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)
            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_by_user_with_limit")
    def test_fetch_query_by_user_with_limit(self) -> None:
        """Success Case: Fetch `Query` records given a user's email
        up to limit."""

        queries = Query.fetch_query(
            user=arguments.FETCH_QUERY_BY_USER, limit=arguments.FETCH_QUERY_WITH_LIMIT
        )

        self.assertIsInstance(queries, QuerySet[QueryModel])

        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_BY_USER_WITH_LIMIT_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            query_id: int = query.id

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)
            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_by_resource_id_for_user_with_limit")
    def test_fetch_query_by_resource_id_for_user_with_limit(self) -> None:
        """Success Case: Fetch `Query` records filtered by `Resource` id and a user's email up to limit."""

        queries = Query.fetch_query(
            resource_id=arguments.FETCH_QUERY_BY_RESOURCE_ID,
            user=arguments.FETCH_QUERY_BY_USER,
            limit=arguments.FETCH_QUERY_WITH_LIMIT,
        )

        self.assertIsInstance(queries, QuerySet[QueryModel])

        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_BY_RESOURCE_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            query_id: int = query.id

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)
            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_by_user_with_page_and_limit")
    def test_fetch_query_by_user_with_page_and_limit(self) -> None:
        """Success Case: Fetch a page of `Query` records given a
        user's email up to limit."""

        queries = Query.fetch_query(
            user=arguments.FETCH_QUERY_BY_USER,
            page=arguments.FETCH_QUERY_WITH_PAGE,
            limit=arguments.FETCH_QUERY_WITH_LIMIT,
        )

        self.assertIsInstance(queries, QuerySet[QueryModel])

        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_BY_USER_WITH_PAGE_AND_LIMIT_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            query_id: int = query.id

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)
            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_by_resource_id_for_user_with_page_and_limit")
    def test_fetch_query_by_resource_id_for_user_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Query` records filtered by `Resource` id and a user's email up to limit."""

        queries = Query.fetch_query(
            resource_id=arguments.FETCH_QUERY_BY_RESOURCE_ID,
            user=arguments.FETCH_QUERY_BY_USER,
            page=arguments.FETCH_QUERY_WITH_PAGE,
            limit=arguments.FETCH_QUERY_WITH_LIMIT,
        )

        self.assertIsInstance(queries, QuerySet[QueryModel])

        self.assertEqual(
            queries.count(),  # type: ignore[union-attr]
            arguments.FETCH_QUERY_BY_RESOURCE_RECORD_COUNT,
        )

        for query in queries:  # type: ignore[union-attr]
            query_id: int = query.id

            self.assertIn(query_id, arguments.VALID_QUERY_RECORDS)
            self.assertEqual(
                QuerySerializer(query).data,
                arguments.VALID_QUERY_RECORDS[query_id],
            )

    @tag("controllers.query.fetch_query_by_id_dne")
    def test_fetch_query_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Query` record given an id where record
        does not exist."""

        with pytest.raises(AnalyticsError):
            _ = Query.fetch_query(record_id=arguments.FETCH_QUERY_BY_ID_DNE)

    @tag("controllers.query.fetch_query_by_resource_id_dne")
    def test_fetch_query_by_resource_id_dne(self) -> None:
        """Fail Case: Fetch `Query` records given a `Resource` id where the `Resource` does not exist."""

        with pytest.raises(AnalyticsError):
            _ = Query.fetch_query(record_id=arguments.FETCH_QUERY_BY_RESOURCE_ID_DNE)

    @tag("controllers.query.fetch_query_by_user_dne")
    def test_fetch_query_by_user_dne(self) -> None:
        """Fail Case: Fetch a `Query` record given a user's email
        where `User` does not exist."""

        with pytest.raises(AnalyticsError):
            _ = Query.fetch_query(user=arguments.FETCH_QUERY_BY_USER_DNE)

    @tag("controllers.query.fetch_query_by_id_with_page")
    def test_fetch_query_by_id_with_page(self) -> None:
        """Fail Case: Fetch a `Query` record given an id where
        a page is also supplied in the parameters."""

        with pytest.raises(AnalyticsError):
            _ = Query.fetch_query(
                record_id=arguments.FETCH_QUERY_BY_ID,
                page=arguments.FETCH_QUERY_WITH_PAGE,
            )

    @tag("controllers.query.fetch_query_by_id_with_limit")
    def test_fetch_query_by_id_with_limit(self) -> None:
        """Fail Case: Fetch a `Query` record given an id where
        a limit is also supplied in the parameters."""

        with pytest.raises(AnalyticsError):
            _ = Query.fetch_query(
                record_id=arguments.FETCH_QUERY_BY_ID,
                limit=arguments.FETCH_QUERY_WITH_LIMIT,
            )

    @tag("controllers.query.fetch_query_by_id_with_page_and_limit")
    def test_fetch_query_by_id_with_page_and_limit(self) -> None:
        """Fail Case: Fetch a `Query` record given an id where
        a page and limit is also supplied in the parameters."""

        with pytest.raises(AnalyticsError):
            _ = Query.fetch_query(
                record_id=arguments.FETCH_QUERY_BY_ID,
                page=arguments.FETCH_QUERY_WITH_PAGE,
                limit=arguments.FETCH_QUERY_WITH_LIMIT,
            )
