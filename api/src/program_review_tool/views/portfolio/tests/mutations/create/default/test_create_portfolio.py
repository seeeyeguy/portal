"""
Collection of pytests for Portfolio's create view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from program_review_tool.controllers.Portfolio.tests.mutations.create.default import (
    arguments,
)

from manager.utils.tests import MultiDBTestCase


@tag(
    "portfolio",
    "program_review_tool",
    "views",
    "portfolio.create.default",
    "program_review_tool.portfolio.create",
    "views.TestCreatePortfolio",
)
class TestCreatePortfolio(MultiDBTestCase):
    """
    Tests for POST /v1/program-review-tool/portfolio endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Portfolio/tests/mutations/create/default/fixtures/programs.json",
        "program_review_tool/controllers/Portfolio/tests/mutations/create/default/fixtures/portfolios.json",
    ]

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(email=arguments.CREATE_PORTFOLIO_USER_EMAIL)
        self.client.force_login(user=user)

    url: str = reverse("program_review_tool.portfolio")

    @tag("views.portfolio.create_portfolio")
    def test_create_portfolio(self) -> None:
        """Success Case: Create a `Portfolio` record."""

        body: dict = {
            "name": arguments.CREATE_PORTFOLIO_NAME,
            "programs": arguments.CREATE_PORTFOLIO_PROGRAM_IDS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        portfolio = response.json()
        del portfolio["created"]
        del portfolio["modified"]

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertDictEqual(portfolio, arguments.CREATE_PORTFOLIO_EXPECTED_PORTFOLIO)

    @tag("views.portfolio.create_portfolio_empty_name")
    def test_create_portfolio_empty_name(self) -> None:
        """Fail Case: Create a `Portfolio` record with
        an empty name."""

        body: dict = {
            "name": "",
            "programs": arguments.CREATE_PORTFOLIO_PROGRAM_IDS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.portfolio.test_create_portfolio_duplicate_name_for_user")
    def test_create_portfolio_with_duplicate_name_for_user(self) -> None:
        """Fail Case: Create a `Portfolio` record with a name
        that already exists for the given `User`."""

        body: dict = {
            "name": arguments.CREATE_PORTFOLIO_DUPLICATE_NAME_FOR_USER,
            "programs": arguments.CREATE_PORTFOLIO_PROGRAM_IDS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.portfolio.create_portfolio_empty_programs")
    def test_create_portfolio_empty_programs(self) -> None:
        """Fail Case: Create a `Portfolio` record without supplying
        `Program` ids."""

        body: dict = {
            "name": arguments.CREATE_PORTFOLIO_NAME,
            "programs": [],
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @tag("views.portfolio.create_portfolio_programs_dne")
    def test_create_portfolio_programs_dne(self) -> None:
        """Fail Case: Create a `Portfolio` record, supplying
        ids for `Program`s that do not exist."""

        body: dict = {
            "name": arguments.CREATE_PORTFOLIO_NAME,
            "programs": arguments.CREATE_PORTFOLIO_PROGRAM_IDS_DNE,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("controllers.portfolio.create_portfolio_user_not_authenticated")
    def test_create_portfolio_user_not_authenticated(self) -> None:
        """Fail Case: Create a `Portfolio` record with a `User`
        that is not authenticated."""

        self.client.logout()

        body: dict = {
            "name": arguments.CREATE_PORTFOLIO_NAME,
            "programs": arguments.CREATE_PORTFOLIO_PROGRAM_IDS,
        }

        response = self.client.post(self.url, body, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
