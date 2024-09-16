"""
`BI Portal` `Profile` view module. Views handle requests to
create, fetch, update, and delete records within the `Profile`
table. `Profile` offers additional information about a user.
"""

import logging

from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from users.views import serializers

from manager.utils.decorators import with_serializer

LOGGER = logging.getLogger(__name__)


class Profile(LoginRequiredMixin, View):
    """
    Handle user requests to fetch `Profile` records for `BI Portal`.
    `Profile` offers additional information about a user.
    """

    @method_decorator(with_serializer(serializers.FetchProfileRequest))
    def get(self, request: http.HttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/users/profile."""

        LOGGER.info(f"GET /v1/users/profile?user={body['user']}.")
        return http.JsonResponse({}, status=status.HTTP_200_OK, safe=False)
