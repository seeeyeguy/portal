"""
Collection of pytests for Query's create controller.
"""

# pylint: disable=wrong-import-order
import pytest
from typing import List

from django.test import tag

from analytics.controllers.Query.Query import Query as QueryController
from analytics.controllers.Query.tests.mutations.create.default import arguments
from analytics.exceptions import AnalyticsError
from analytics.models.Query.Query import Query as QueryModel
from analytics.models.Query.serializers import QuerySerializer

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "analytics",
    "query",
    "controllers.TestCreateQuery",
    "analytics.query.create",
    "query.create.default",
)
class TestCreateQuery(MultiDBTestCase):
    """Test suite for Query's create controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "analytics/controllers/Query/tests/mutations/create/default/fixtures/resources.json",
        "analytics/controllers/Query/tests/mutations/create/default/fixtures/pointofcontacts.json",
        "analytics/controllers/Query/tests/mutations/create/default/fixtures/requests.json",
        "analytics/controllers/Query/tests/mutations/create/default/fixtures/transitions.json",
        "analytics/controllers/Query/tests/mutations/create/default/fixtures/dispositions.json",
    ]

    @tag("controllers.query.create_query")
    def test_create_query(self) -> None:
        """Success Case: Create a `Query` record."""

        query = QueryController.create_query(
            user=arguments.CREATE_QUERY_USER_EMAIL,
            search_term=arguments.CREATE_QUERY_SEARCH_TERM,
        )

        self.assertIsInstance(query, QueryModel)

        serialized_query = QuerySerializer(query).data
        del serialized_query["created"]
        del serialized_query["id"]

        self.assertEqual(serialized_query, arguments.VALID_CREATED_QUERY)

    @tag("controllers.query.create_query_search_term_no_results")
    def test_create_query_search_term_no_results(self) -> None:
        """Success Case: Create a `Query` record with a search term
        that yielded no results."""

        query = QueryController.create_query(
            user=arguments.CREATE_QUERY_USER_EMAIL,
            search_term=arguments.SEARCH_TERM_NO_RESULTS,
        )

        self.assertIsInstance(query, QueryModel)

        serialized_query = QuerySerializer(query).data
        del serialized_query["created"]
        del serialized_query["id"]

        self.assertEqual(serialized_query, arguments.VALID_NO_RESULTS_QUERY)

    @tag("controllers.query.create_query_user_dne")
    def test_create_query_user_dne(self) -> None:
        """Fail Case: Create a `Query` record with a `User`
        that does not exist."""

        with pytest.raises(AnalyticsError):
            QueryController.create_query(
                user=arguments.CREATE_QUERY_USER_EMAIL_DNE,
                search_term=arguments.CREATE_QUERY_SEARCH_TERM,
            )
