"""
Collection of pytests for Portfolio's fetch controller.
"""

import pytest
from typing import cast, List, Dict, Union

from django.contrib.auth import models as AuthModels
from django.db.models import QuerySet
from django.test import tag

from program_review_tool import controllers, exceptions, models
from program_review_tool.controllers.Portfolio.tests.query.read.default import arguments
from program_review_tool.models.Portfolio.serializers import PortfolioSerializer

from manager.utils.tests import MultiDBTestCase


@tag(
    "controllers",
    "portfolio",
    "program_review_tool",
    "controllers.TestFetchPortfolio",
    "portfolio.fetch.default",
    "program_review_tool.portfolio.fetch",
)
class TestFetchPortfolio(MultiDBTestCase):
    """Test suite for Portfolio's fetch controller."""

    fixtures: List[str] = [
        "portal/models/fixtures/segments/segments.json",
        "portal/models/fixtures/users/users.json",
        "program_review_tool/controllers/Portfolio/tests/query/read/default/fixtures/programs.json",
        "program_review_tool/controllers/Portfolio/tests/query/read/default/fixtures/portfolios.json",
    ]

    @tag("controllers.portfolio.fetch_portfolios_by_user")
    def test_fetch_portfolios_by_user(self) -> None:
        """Success Case: Fetch all `Portfolio` records for
        the given user."""

        # Query user from db.
        user = AuthModels.User.objects.get(
            username=arguments.FETCH_PORTFOLIO_USER_EMAIL
        )

        # Fetch portfolios for user.
        portfolios = controllers.Portfolio.fetch_portfolios(user=user)

        # Ensure data is a `Portfolio` queryset.
        self.assertIsInstance(portfolios, QuerySet[models.Portfolio])

        data: List[Dict[str, Union[bool, int, str]]] = PortfolioSerializer(
            portfolios, many=True
        ).data

        # Ensure the data is correct.
        self.assertEqual(data, arguments.EXPECTED_PORTFOLIOS)

    @tag("controllers.portfolio.fetch_portfolios_by_user_not_authenticated")
    def test_fetch_portfolios_by_user_not_authenticated(self) -> None:
        """Fail Case: Fetch all `Portfolio` records for
        a `User` that is not authenticated."""

        with pytest.raises(exceptions.ProgramReviewToolError):
            controllers.Portfolio.fetch_portfolios(
                user=cast(AuthModels.User, AuthModels.AnonymousUser())
            )
