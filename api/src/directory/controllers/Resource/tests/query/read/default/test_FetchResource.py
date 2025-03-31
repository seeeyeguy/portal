"""
Collection of pytests for Resource's fetch controller.
"""

# pylint: disable=line-too-long,wrong-import-order
import pytest
from typing import List

from django.db.models import QuerySet
from django.test import tag

from directory.controllers.Resource.Resource import Resource
from directory.controllers.Resource.tests.query.read.default import arguments
from directory.exceptions import DirectoryError
from directory.models.Resource.Resource import Resource as ResourceModel
from directory.models.Resource.serializers import ResourceSerializer

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "directory",
    "resource",
    "controllers.TestFetchResource",
    "directory.resource.fetch",
    "resource.fetch.default",
)
class TestFetchResource(MultiDBTestCase):
    """Test suite for Resource's fetch controller."""

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "directory/controllers/Resource/tests/query/read/default/fixtures/resources.json",
        "directory/controllers/Resource/tests/query/read/default/fixtures/requests.json",
        "directory/controllers/Resource/tests/query/read/default/fixtures/transitions.json",
        "directory/controllers/Resource/tests/query/read/default/fixtures/dispositions.json",
    ]

    @tag("controllers.resource.fetch_resources")
    def test_fetch_resources(self) -> None:
        """Success Case: Fetch all `Resource` records."""

        resources = Resource.fetch_resources()

        self.assertIsInstance(resources, QuerySet[ResourceModel])
        self.assertEqual(
            resources.count(), len(arguments.VALID_RESOURCE_RECORDS)  # type: ignore[union-attr]
        )

        for resource in resources:  # type: ignore[union-attr]
            self.assertIsInstance(resource, ResourceModel)

            resource_id: int = resource.id

            self.assertIn(resource_id, arguments.VALID_RESOURCE_RECORDS)
            self.assertEqual(
                ResourceSerializer(resource).data,
                arguments.VALID_RESOURCE_RECORDS[resource_id],
            )

    @tag("controllers.resource.fetch_resources_with_page")
    def test_fetch_resources_with_page(self) -> None:
        """Success Case: Fetch page of `Resource` records."""

        resources = Resource.fetch_resources(page=arguments.FETCH_RESOURCE_WITH_PAGE)

        self.assertIsInstance(resources, QuerySet[ResourceModel])
        self.assertEqual(resources.count(), len(arguments.VALID_RESOURCE_RECORDS))  # type: ignore[union-attr]

        for resource in resources:  # type: ignore[union-attr]
            self.assertIsInstance(resource, ResourceModel)

            resource_id: int = resource.id

            self.assertIn(resource_id, arguments.VALID_RESOURCE_RECORDS)
            self.assertEqual(
                ResourceSerializer(resource).data,
                arguments.VALID_RESOURCE_RECORDS[resource_id],
            )

    @tag("controllers.resource.fetch_resources_with_limit")
    def test_fetch_resources_with_limit(self) -> None:
        """Success Case: Fetch all `Resource` records up to limit."""

        resources = Resource.fetch_resources(limit=arguments.FETCH_RESOURCE_WITH_LIMIT)

        self.assertIsInstance(resources, QuerySet[ResourceModel])
        self.assertEqual(resources.count(), len(arguments.FETCH_RESOURCE_WITH_LIMIT_VALID_IDS))  # type: ignore[union-attr]

        for resource in resources:  # type: ignore[union-attr]
            self.assertIsInstance(resource, ResourceModel)

            resource_id: int = resource.id

            self.assertIn(resource_id, arguments.FETCH_RESOURCE_WITH_LIMIT_VALID_IDS)
            self.assertEqual(
                ResourceSerializer(resource).data,
                arguments.VALID_RESOURCE_RECORDS[resource_id],
            )

    @tag("controllers.resource.fetch_resources_with_page_and_limit")
    def test_fetch_resources_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Resource` records up to limit."""

        resources = Resource.fetch_resources(
            page=arguments.FETCH_RESOURCE_WITH_PAGE,
            limit=arguments.FETCH_RESOURCE_WITH_PAGE_AND_LIMIT_LIMIT_NUMBER,
        )

        self.assertIsInstance(resources, QuerySet[ResourceModel])
        self.assertEqual(resources.count(), len(arguments.FETCH_RESOURCE_WITH_PAGE_AND_LIMIT_VALID_IDS))  # type: ignore[union-attr]

        for resource in resources:  # type: ignore[union-attr]
            self.assertIsInstance(resource, ResourceModel)

            resource_id: int = resource.id

            self.assertIn(
                resource_id, arguments.FETCH_RESOURCE_WITH_PAGE_AND_LIMIT_VALID_IDS
            )
            self.assertEqual(
                ResourceSerializer(resource).data,
                arguments.VALID_RESOURCE_RECORDS[resource_id],
            )

    @tag("controllers.resource.fetch_resources_with_page_exceeding_page_count")
    def test_fetch_resources_with_page_exceeding_page_count(self) -> None:
        """Success Case: Fetch page of `Resource` records using a
        page number that exceeds the number of pages."""

        resources = Resource.fetch_resources(
            page=arguments.FETCH_RESOURCE_WITH_PAGE_EXCEEDING_PAGE_COUNT
        )

        self.assertIsInstance(resources, QuerySet[ResourceModel])
        self.assertEqual(
            resources.count(),  # type: ignore[union-attr]
            arguments.FETCH_RESOURCE_WITH_PAGE_EXCEEDING_PAGE_COUNT_RECORD_COUNT,
        )

    @tag("controllers.resource.fetch_resource_by_id")
    def test_fetch_resource_by_id(self) -> None:
        """Success Case: Fetch a `Resource` record given an id."""

        resource = Resource.fetch_resources(resource_id=arguments.FETCH_RESOURCE_BY_ID)

        self.assertIsInstance(resource, ResourceModel)

        resource_id: int = resource.id  # type: ignore[union-attr]

        self.assertIn(resource_id, arguments.VALID_RESOURCE_RECORDS)
        self.assertEqual(
            ResourceSerializer(resource).data,
            arguments.VALID_RESOURCE_RECORDS[resource_id],
        )

    @tag("controllers.resource.fetch_resource_by_id_dne")
    def test_fetch_resource_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Resource` record given an id where
        the record does not exist."""

        with pytest.raises(DirectoryError):
            _ = Resource.fetch_resources(resource_id=arguments.FETCH_RESOURCE_BY_ID_DNE)

    @tag("controllers.resource.fetch_resource_by_id_with_page")
    def test_fetch_resource_by_id_with_page(self) -> None:
        """Fail Case: Fetch a `Resource` record given an id where
        a page is also supplied in the parameters."""

        with pytest.raises(DirectoryError):
            _ = Resource.fetch_resources(
                resource_id=arguments.FETCH_RESOURCE_BY_ID,
                page=arguments.FETCH_RESOURCE_WITH_PAGE,
            )

    @tag("controllers.resource.fetch_resource_by_id_with_limit")
    def test_fetch_resource_by_id_with_limit(self) -> None:
        """Fail Case: Fetch a `Resource` record given an id where
        a limit is also supplied in the parameters."""

        with pytest.raises(DirectoryError):
            _ = Resource.fetch_resources(
                resource_id=arguments.FETCH_RESOURCE_BY_ID,
                limit=arguments.FETCH_RESOURCE_WITH_LIMIT,
            )

    @tag("controllers.resource.fetch_resource_by_id_with_page_and_limit")
    def test_fetch_resource_by_id_with_page_and_limit(self) -> None:
        """Fail Case: Fetch a `Resource` record given an id where
        a page and limit is also supplied in the parameters."""

        with pytest.raises(DirectoryError):
            _ = Resource.fetch_resources(
                resource_id=arguments.FETCH_RESOURCE_BY_ID,
                page=arguments.FETCH_RESOURCE_WITH_PAGE,
                limit=arguments.FETCH_RESOURCE_WITH_LIMIT,
            )
