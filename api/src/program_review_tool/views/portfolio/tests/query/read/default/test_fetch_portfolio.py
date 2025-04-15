"""
Collection of pytests for Portfolio's fetch view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from program_review_tool.controllers.Portfolio.tests.query.read.default import arguments

from manager.utils.tests import MultiDBTestCase


@tag(
    "portfolio",
    "program_review_tool",
    "views",
    "portfolio.fetch.default",
    "program_review_tool.portfolio.fetch",
    "views.TestFetchPortfolio",
)
class TestFetchPortfolio(MultiDBTestCase):
    """
    Tests for GET /v1/program-review-tool/portfolio endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Portfolio/tests/query/read/default/fixtures/programs.json",
        "program_review_tool/controllers/Portfolio/tests/query/read/default/fixtures/portfolios.json",
    ]

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(email=arguments.FETCH_PORTFOLIO_USER_EMAIL)
        self.client.force_login(user=user)

    url: str = reverse("program_review_tool.portfolio")

    @tag("views.portfolio.fetch_portfolios_by_user")
    def test_fetch_portfolios_by_user(self) -> None:
        """Success Case: Fetch all `Portfolio` records for
        the given user."""

        params: dict = {"user": arguments.FETCH_PORTFOLIO_USER_EMAIL}

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        portfolios = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(portfolios, list)

        self.assertEqual(
            len(portfolios), arguments.FETCH_PORTFOLIOS_EXPECTED_PORTFOLIOS_COUNT
        )

        for portfolio in portfolios:
            portfolio_id: int = portfolio["id"]

            expected = next(
                (
                    record
                    for record in arguments.FETCH_PORTFOLIOS_EXPECTED_PORTFOLIOS
                    if record["id"] == portfolio_id
                ),
                None,
            )

            self.assertIsInstance(portfolio, dict)

            self.assertEqual(
                portfolio,
                expected,
            )

    @tag("views.portfolio.fetch_portfolios_by_user_permissions_denied")
    def test_fetch_portfolios_by_user_permissions_denied(self) -> None:
        """Fail Case: Fetch all `Portfolio` records for the wrong
        `User`."""

        params = {"user": arguments.FETCH_PORTFOLIO_USER_EMAIL_PERMISSIONS_DENIED}

        response = self.client.get(
            self.url, params, headers={"content_type": "application/json"}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
