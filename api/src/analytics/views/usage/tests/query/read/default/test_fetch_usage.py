"""
Collection of pytests for Usages fetch view.
"""
import pytest
from typing import List

from django.urls import reverse
from django.contrib.auth import models as AuthModels

from rest_framework import status
from program_review_tool.controllers.Usage.tests.query.read.default import arguments
from manager.utils.tests import MultiDBTestCase


class TestUsageFetchView(MultiDBTestCase):
    fixtures: List[str] = [
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Usage/tests/query/read/default/fixtures/usage_data.json",
    ]

    def setUp(self) -> None:
        super().setUp()
        user = AuthModels.User.objects.get(username=arguments.FETCH_USAGE_USER)
        self.client.force_login(user=user)

    url: str = reverse("analytics.prt.usage")

    def test_fetch_usage_view_success(self) -> None:
        """Success Case: Fetch Usage records for a valid user without pagination."""
        params: dict = {"user": arguments.FETCH_USAGE_USER}
        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )
        usage_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(usage_data, list)
        self.assertEqual(len(usage_data), arguments.FETCH_USAGE_RECORD_COUNT)

        for usage in usage_data:
            usage_id: int = usage["id"]
            expected = arguments.FETCH_USAGE_EXPECTED_RECORDS.get(usage_id)
            del usage["created"]
            self.assertIsInstance(usage, dict)
            self.assertEqual(usage, expected)

    def test_fetch_usage_view_with_page_and_limit(self) -> None:
        """Success Case: Fetch Usage records with valid page + limit pagination."""
        params: dict = {
            "user": arguments.FETCH_USAGE_USER,
            "page": arguments.FETCH_USAGE_PAGE,
            "limit": arguments.FETCH_USAGE_LIMIT,
        }
        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )
        usage_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(usage_data), arguments.FETCH_USAGE_LIMIT)

    def test_fetch_usage_view_with_limit_only(self) -> None:
        """Success Case: Fetch Usage records with only limit applied."""
        params: dict = {
            "user": arguments.FETCH_USAGE_USER,
            "limit": arguments.FETCH_USAGE_LIMIT,
        }
        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )
        usage_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(usage_data), arguments.FETCH_USAGE_LIMIT)

    def test_fetch_usage_view_invalid_user(self) -> None:
        """Fail Case: Attempt to fetch Usage records for an invalid user email."""
        params: dict = {"user": arguments.INVALID_USER}
        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_fetch_usage_view_with_negative_page(self) -> None:
        """Fail Case: Page must be a positive integer."""
        params: dict = {
            "user": arguments.FETCH_USAGE_USER,
            "page": arguments.INVALID_USAGE_PAGE,
            "limit": arguments.FETCH_USAGE_LIMIT,
        }
        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fetch_usage_view_with_negative_limit(self) -> None:
        """Fail Case: Limit must be a positive integer."""
        params: dict = {
            "user": arguments.FETCH_USAGE_USER,
            "page": arguments.FETCH_USAGE_PAGE,
            "limit": arguments.INVALID_USAGE_LIMIT,
        }
        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fetch_usage_view_with_pa_number(self) -> None:
        """Success Case: Fetch Usage records filtered by a specific PA number."""
        params: dict = {
            "user": arguments.FETCH_USAGE_USER,
            "pa_number": arguments.FETCH_USAGE_PA_NUMBER,
        }
        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )
        usage_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure all returned usages include the PA number
        for usage in usage_data:
            self.assertIn(arguments.FETCH_USAGE_PA_NUMBER, usage["programs"])

    def test_fetch_usage_view_invalid_user(self) -> None:
        """Fail Case: Fetch Usage records for an invalid user should return 404."""
        params: dict = {"user": arguments.INVALID_USER}
        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fetch_usage_view_success_true(self) -> None:
        """Success Case: Fetch Usage records where success=True."""
        params: dict = {
            "user": arguments.FETCH_USAGE_USER,
            "success": arguments.FETCH_USAGE_SUCCESS_TRUE,
        }
        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )
        usage_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for usage in usage_data:
            self.assertTrue(usage["success"])
