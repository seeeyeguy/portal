"""
Collection of pytests for Portfolio's delete view endpoint.
"""

from typing import List

# pylint: disable=line-too-long
from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from program_review_tool.controllers.Portfolio.tests.mutations.delete.default import (
    arguments,
)

from manager.utils.tests import MultiDBTestCase


@tag(
    "portfolio",
    "program_review_tool",
    "views",
    "portfolio.delete.default",
    "program_review_tool.portfolio.delete",
    "views.TestDeletePortfolio",
)
class TestDeletePortfolio(MultiDBTestCase):
    """
    Tests for DELETE /v1/program-review-tool/portfolio endpoint.
    """

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Portfolio/tests/mutations/delete/default/fixtures/programs.json",
        "program_review_tool/controllers/Portfolio/tests/mutations/delete/default/fixtures/portfolios.json",
    ]

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(email=arguments.DELETE_PORTFOLIO_USER_EMAIL)
        self.client.force_login(user=user)

    url: str = reverse("program_review_tool.portfolio")

    @tag("views.portfolio.delete_portfolio")
    def test_delete_portfolio(self) -> None:
        """Success Case: Delete a `Portfolio` record with given id."""

        response = self.client.delete(
            f"{self.url}?id={arguments.DELETE_PORTFOLIO_PORTFOLIO_ID}",
            headers={"content_type": "application/json"},
        )

        rows_affected = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(rows_affected, 1)

    @tag("views.portfolio.delete_portfolio_user_not_authenticated")
    def test_delete_portfolio_user_not_authenticated(self) -> None:
        """Fail Case: Delete a `Portfolio` record with an unauthenticated user."""

        self.client.logout()

        response = self.client.delete(
            f"{self.url}?id={arguments.DELETE_PORTFOLIO_PORTFOLIO_ID}",
            headers={"content_type": "application/json"},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
