"""
Collection of pytests for Portfolio's update view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from program_review_tool.controllers.Portfolio.tests.mutations.update.default import (
    arguments,
)

from manager.utils.tests import MultiDBTestCase


@tag(
    "portfolio",
    "program_review_tool",
    "views",
    "portfolio.update.default",
    "program_review_tool.portfolio.update",
    "views.TestUpdatePortfolio",
)
class TestUpdatePortfolio(MultiDBTestCase):
    """
    Tests for PUT /v1/program-review-tool/portfolio endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Portfolio/tests/mutations/update/default/fixtures/portfolios.json",
        "program_review_tool/controllers/Portfolio/tests/mutations/update/default/fixtures/programs.json",
        "program_review_tool/controllers/Portfolio/tests/mutations/update/default/fixtures/segments.json",
    ]

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(
            username=arguments.UPDATE_PORTFOLIO_USER_EMAIL
        )
        self.client.force_login(user=user)

    url: str = reverse("program_review_tool.portfolio")

    @tag("views.portfolio.update_portfolio")
    def test_update_portfolio(self) -> None:
        """Success Case: Update a `Portfolio` record."""

        body: dict = {
            "name": arguments.UPDATE_PORTFOLIO_PORTFOLIO_NAME,
            "programs": arguments.UPDATE_PORTFOLIO_PROGRAM_IDS,
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_PORTFOLIO_PORTFOLIO_ID}"

        response = self.client.put(request_url, body, content_type="application/json")

        portfolio = response.json()

        # Remove dynamic datetime fields before comparison
        del portfolio["created"]
        del portfolio["modified"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertDictEqual(portfolio, arguments.UPDATE_PORTFOLIO_EXPECTED_PORTFOLIO)

    @tag("views.portfolio.update_portfolio_dne")
    def test_update_portfolio_record_dne(self) -> None:
        """Fail Case: Update a `Portfolio` record that
        does not exist."""

        body: dict = {
            "name": arguments.UPDATE_PORTFOLIO_PORTFOLIO_NAME,
            "programs": arguments.UPDATE_PORTFOLIO_PROGRAM_IDS,
        }

        request_url: str = (
            f"{self.url}?id={arguments.UPDATE_PORTFOLIO_PORTFOLIO_ID_DNE}"
        )

        response = self.client.put(request_url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("views.portfolio.update_portfolio_duplicate_name")
    def test_update_portfolio_duplicate_name(self) -> None:
        """Fail Case: Update a `Portfolio` record with
        a duplicate name for the given user."""

        body: dict = {
            "name": arguments.UPDATE_PORTFOLIO_DUPLICATE_PORTFOLIO_NAME_FOR_USER,
            "programs": arguments.UPDATE_PORTFOLIO_PROGRAM_IDS,
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_PORTFOLIO_DUPLICATE_PORTFOLIO_NAME_FOR_USER_PORTFOLIO_ID}"

        response = self.client.put(request_url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.portfolio.update_portfolio_empty_programs")
    def test_update_portfolio_empty_programs(self) -> None:
        """Fail Case: Update a `Portfolio` record without supplying
        `Program` ids."""

        body: dict = {
            "name": arguments.UPDATE_PORTFOLIO_PORTFOLIO_NAME,
            "programs": [],
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_PORTFOLIO_PORTFOLIO_ID}"

        response = self.client.put(request_url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.portfolio.update_portfolio_programs_dne")
    def test_update_portfolio_programs_dne(self) -> None:
        """Fail Case: Update a `Portfolio` record, supplying
        ids for `Program`s that do not exist."""

        body: dict = {
            "name": arguments.UPDATE_PORTFOLIO_PORTFOLIO_NAME,
            "programs": arguments.UPDATE_PORTFOLIO_PROGRAM_IDS_DNE,
        }

        request_url: str = f"{self.url}?id={arguments.UPDATE_PORTFOLIO_PORTFOLIO_ID}"

        response = self.client.put(request_url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("controllers.portfolio.update_portfolio_user_not_authenticated")
    def test_update_portfolio_user_not_authenticated(self) -> None:
        """Fail Case: Update a `Portfolio` record with a `User`
        that is not authenticated."""

        self.client.logout()

        body: dict = {
            "name": arguments.UPDATE_PORTFOLIO_PORTFOLIO_NAME,
            "programs": arguments.UPDATE_PORTFOLIO_PROGRAM_IDS,
        }

        response = self.client.put(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
