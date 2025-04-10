"""
`Program Review Tool` `Portfolio` view module. Views handle requests to
create, fetch, update, and delete records within the `Portfolio`
table.
"""

import logging
from typing import List

from django import http
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from program_review_tool import controllers, exceptions
from program_review_tool.models.Portfolio.serializers import PortfolioSerializer
from program_review_tool.views import serializers

from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


class Portfolio(View):
    """
    Handle user requests to create, fetch, update,
    and delete `Portfolio` records for `Program Review Tool`.
    """

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.CreatePortfolioRequest))
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /program-review-tool/portfolio."""

        LOGGER.info("POST /program-review-tool/portfolio.")

        try:
            # Create `Portfolio`.
            portfolio = controllers.Portfolio.create_portfolio(
                user=request.user, programs=body["programs"], name=body["name"]
            )

            # Serialize `Portfolio`.
            data: dict = PortfolioSerializer(portfolio).data

            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
        except exceptions.ProgramReviewToolError as exc:
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.UpdatePortfolioRequest))
    def put(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for PUT /program-review-tool/portfolio."""

        try:
            req = serializers.UpdatePortfolioRequestQueryParams(data=request.GET)

            if not req.is_valid():
                return http.JsonResponse(
                    req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
                )

            portfolio_id: int = req.validated_data.get("id")

            LOGGER.info(f"PUT /program-review-tool/portfolio?id={portfolio_id}.")

            # Update `Portfolio`.
            portfolio = controllers.Portfolio.update_portfolio(
                portfolio_id=portfolio_id,
                name=body["name"],
                programs=body["programs"],
            )

            # Serialize `Portfolio`.
            data: dict = PortfolioSerializer(portfolio).data

            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
        except exceptions.ProgramReviewToolError as exc:
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    def delete(self, request: DjangoHttpRequest) -> http.JsonResponse:
        """Endpoint for DELETE /v1/program-review-tool/portfolio."""

        try:
            req = serializers.DeletePortfolioRequestQueryParams(data=request.GET)

            if not req.is_valid():
                return http.JsonResponse(
                    req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
                )

            portfolio_id: int = req.validated_data.get("id")

            LOGGER.info(f"DELETE /program-review-tool/portfolio?id={portfolio_id}.")

            rows_affected = controllers.Portfolio.delete_portfolio(
                portfolio_id=portfolio_id
            )

            return http.JsonResponse(
                rows_affected, status=status.HTTP_200_OK, safe=False
            )
        except exceptions.ProgramReviewToolError as exc:
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    def get(self, request: DjangoHttpRequest) -> http.JsonResponse:
        """Endpoint for GET /v1/program-review-tool/portfolio."""

        try:
            req = serializers.FetchPortfolioRequestQueryParams(data=request.GET)

            if not req.is_valid():
                return http.JsonResponse(
                    req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
                )

            user = req.validated_data.get("user")

            if request.user.username != user:
                return http.JsonResponse(
                    "Permissions Denied.", status=status.HTTP_403_FORBIDDEN, safe=False
                )

            LOGGER.info(f"GET /program-review-tool/portfolio?user={user}")

            # Fetch the `Portfolio`(s).
            portfolios = controllers.Portfolio.fetch_portfolios(request.user)

            # Serialize `Portfolio`(s).
            data: List[dict] = PortfolioSerializer(portfolios, many=True).data

            return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except exceptions.ProgramReviewToolError as exc:
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
