"""
Collection of pytests for Resource's fetch view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag, TestCase
from django.urls import reverse
from rest_framework import status

from directory.controllers.Resource.tests.query.read.default import arguments

from portal.models.fixtures import COMMON_FIXTURES


@tag(
    "directory",
    "resource",
    "views",
    "directory.resource.fetch",
    "resource.fetch.default",
    "views.TestFetchResources",
)
class TestFetchResource(TestCase):
    """
    Tests for GET /v1/directory/resources endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(email=arguments.FETCH_RESOURCE_BY_USER)
        self.client.force_login(user=user)

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "directory/controllers/Resource/tests/query/read/default/fixtures/resources.json",
        "directory/controllers/Resource/tests/query/read/default/fixtures/requests.json",
        "directory/controllers/Resource/tests/query/read/default/fixtures/transitions.json",
        "directory/controllers/Resource/tests/query/read/default/fixtures/dispositions.json",
    ]

    url: str = reverse("directory.resource")

    @tag("views.resource.fetch_resources")
    def test_fetch_resources(self) -> None:
        """Success Case: Fetch all `Resource` records."""

        response = self.client.get(
            self.url, headers={"content_type": "application/json"}
        )

        resources = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(resources, list)

        self.assertEqual(len(resources), arguments.FETCH_RESOURCE_RECORD_COUNT)

        for resource in resources:
            resource_id: int = resource["id"]

            self.assertIsInstance(resource, dict)

            self.assertIn(resource_id, arguments.VALID_RESOURCE_RECORDS)

            self.assertEqual(
                resource,
                arguments.VALID_RESOURCE_RECORDS[resource_id],
            )

    @tag("views.resource.fetch_resources_with_page")
    def test_fetch_resources_with_page(self) -> None:
        """Success Case: Fetch page of `Resource` records."""

        resource_params: dict = {"page": arguments.FETCH_RESOURCE_WITH_PAGE}

        response = self.client.get(
            self.url, resource_params, headers={"content_type": "application/json"}
        )

        resources = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(resources, list)

        self.assertEqual(
            len(resources), arguments.FETCH_RESOURCE_WITH_PAGE_RECORD_COUNT
        )

        for resource in resources:
            resource_id: int = resource["id"]

            self.assertIsInstance(resource, dict)

            self.assertIn(resource_id, arguments.VALID_RESOURCE_RECORDS)

            self.assertEqual(resource, arguments.VALID_RESOURCE_RECORDS[resource_id])

    @tag("views.resource.fetch_resources_with_limit")
    def test_fetch_resources_with_limit(self) -> None:
        """Success Case: Fetch all `Resource` records up to limit."""

        resource_params: dict = {"limit": arguments.FETCH_RESOURCE_WITH_LIMIT}

        response = self.client.get(
            self.url, resource_params, headers={"content_type": "application/json"}
        )

        resources = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(resources, list)

        self.assertEqual(
            len(resources), arguments.FETCH_RESOURCE_WITH_LIMIT_RECORD_COUNT
        )

        for resource in resources:
            resource_id: int = resource["id"]

            self.assertIsInstance(resource, dict)

            self.assertIn(resource_id, arguments.VALID_RESOURCE_RECORDS)

            self.assertEqual(resource, arguments.VALID_RESOURCE_RECORDS[resource_id])

    @tag("views.resource.fetch_resources_with_page_and_limit")
    def test_fetch_resources_with_page_and_limit(self) -> None:
        """Success Case: Fetch page of `Resource` records up to limit."""

        resource_params: dict = {
            "limit": arguments.FETCH_RESOURCE_WITH_LIMIT,
            "page": arguments.FETCH_RESOURCE_WITH_PAGE,
        }

        response = self.client.get(
            self.url, resource_params, headers={"content_type": "application/json"}
        )

        resources = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(resources, list)

        self.assertEqual(
            len(resources), arguments.FETCH_RESOURCE_WITH_PAGE_AND_LIMIT_RECORD_COUNT
        )

        for resource in resources:
            resource_id: int = resource["id"]

            self.assertIsInstance(resource, dict)

            self.assertIn(resource_id, arguments.VALID_RESOURCE_RECORDS)

            self.assertEqual(
                resource,
                arguments.VALID_RESOURCE_RECORDS[resource_id],
            )

    @tag("views.resource.fetch_resources_with_page_exceeding_page_count")
    def test_fetch_resources_with_page_exceeding_page_count(self) -> None:
        """Success Case: Fetch page of `Resource` records using a
        page number that exceeds the number of pages."""

        resource_params: dict = {
            "page": arguments.FETCH_RESOURCE_WITH_PAGE_EXCEEDING_PAGE_COUNT
        }

        response = self.client.get(
            self.url, resource_params, headers={"content_type": "application/json"}
        )

        resources = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(resources, List)

        self.assertEqual(
            len(resources),
            arguments.FETCH_RESOURCE_WITH_PAGE_EXCEEDING_PAGE_COUNT_RECORD_COUNT,
        )

    @tag("views.resource.fetch_resource_by_id")
    def test_fetch_resource_by_id(self) -> None:
        """Success Case: Fetch a `Resource` record given an id."""

        resource_params: dict = {
            "id": arguments.FETCH_RESOURCE_BY_ID,
        }

        response = self.client.get(
            self.url, resource_params, headers={"content_type": "application/json"}
        )

        resource = response.json()

        self.assertIsInstance(resource, dict)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        resource_id: int = resource["id"]

        self.assertIn(resource_id, arguments.VALID_RESOURCE_RECORDS)

        self.assertEqual(
            resource,
            arguments.VALID_RESOURCE_RECORDS[resource_id],
        )

    @tag("views.resource.fetch_resource_by_id_dne")
    def test_fetch_resource_by_id_dne(self) -> None:
        """Fail Case: Fetch a `Resource` record given an id where
        record does not exist."""

        resource_params: dict = {
            "id": arguments.FETCH_RESOURCE_BY_ID_DNE,
        }

        response = self.client.get(
            self.url, resource_params, headers={"content_type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.resource.fetch_resource_by_id_with_page")
    def test_fetch_resource_by_id_with_page(self) -> None:
        """Fail Case: Fetch a `Resource` record given an id where
        a page is also supplied in the parameters."""

        resource_params: dict = {
            "id": arguments.FETCH_RESOURCE_BY_ID,
            "page": arguments.FETCH_RESOURCE_WITH_PAGE,
        }

        response = self.client.get(
            self.url, resource_params, headers={"content_type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.fetch_resource_by_id_with_limit")
    def test_fetch_resource_by_id_with_limit(self) -> None:
        """Fail Case: Fetch a `Resource` record given an id where
        a limit is also supplied in the parameters."""

        resource_params: dict = {
            "id": arguments.FETCH_RESOURCE_BY_ID,
            "limit": arguments.FETCH_RESOURCE_WITH_LIMIT,
        }

        response = self.client.get(
            self.url, resource_params, headers={"content_type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.resource.fetch_resource_by_id_with_page_and_limit")
    def test_fetch_resource_by_id_with_page_and_limit(self) -> None:
        """Fail Case: Fetch a `Resource` record given an id where
        a page and limit is also supplied in the parameters."""

        resource_params: dict = {
            "id": arguments.FETCH_RESOURCE_BY_ID,
            "page": arguments.FETCH_RESOURCE_WITH_PAGE,
            "limit": arguments.FETCH_RESOURCE_WITH_LIMIT,
        }

        response = self.client.get(
            self.url, resource_params, headers={"content_type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
