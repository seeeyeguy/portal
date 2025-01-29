"""
`BI Portal` `Profile` view module. Views handle requests to
create, fetch, update, and delete records within the `Profile`
table. `Profile` offers additional information about a user.
"""

import logging

from django import http
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from users import controllers, exceptions
from users.models.Profile.serializers import ProfileSerializer
from users.views import serializers

from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


class Profile(View):
    """
    Handle user requests to fetch `Profile` records for `BI Portal`.
    `Profile` offers additional information about a user.
    """

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.FetchProfileRequest))
    def get(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/users/profile."""

        try:
            LOGGER.info(f"GET /v1/users/profile?user={body['user']}.")

            # Deny request if user does not have permissions.
            if request.user.email != body["user"] and not request.user.is_superuser:
                return http.JsonResponse(
                    "Permissions Denied.",
                    status=status.HTTP_403_FORBIDDEN,
                    safe=False,
                )

            # Fetch `Profile` record for the given user.
            profile = controllers.Profile.fetch_profile(user=body["user"])
            # Serialize `Profile`.
            data: dict = ProfileSerializer(profile).data
            return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except exceptions.UsersError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
