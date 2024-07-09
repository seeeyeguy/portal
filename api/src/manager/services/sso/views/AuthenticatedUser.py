"""
API view module for SSO service. Module provides
`AuthenticatedUser` view to process an authentication
check request from the client. If the client is not authenticated,
the view returns a proxy url that may be used for redirection
to the SSO service (ADFS). If the client is authenticated, the 
view will return relevant user data. 
"""

import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from manager.settings import (
    ApplicationBuild,
    BUILD,
    SSO_DEVELOPMENT_USER,
    SSO_DEVELOPMENT_USER_REQUEST_HEADERS_KEY,
    SSO_SERVICE_APP_URL,
)
from manager.utils.types import request


class AuthenticatedUser(APIView):
    """View to manage an authenticated user."""

    def get(self, request: request.DjangoHttpRequest) -> Response:
        """Return the data for an authenticated user, else redirect to SSO."""

        data = {
            "first_name": SSO_DEVELOPMENT_USER["first_name"],
            "last_name": SSO_DEVELOPMENT_USER["last_name"],
            "email": (
                f"{SSO_DEVELOPMENT_USER['first_name']}."
                f"{SSO_DEVELOPMENT_USER['last_name']}@l3harris.com"
            ),
            "is_superuser": True,
        }

        if BUILD == ApplicationBuild.DEVELOPMENT:
            if SSO_DEVELOPMENT_USER_REQUEST_HEADERS_KEY in request.headers:
                dev_user_from_request = json.loads(
                    request.headers[SSO_DEVELOPMENT_USER_REQUEST_HEADERS_KEY]
                )
                data["first_name"] = dev_user_from_request["first_name"]
                data["last_name"] = dev_user_from_request["last_name"]
                data["email"] = dev_user_from_request["email"]

            return Response(data, status=status.HTTP_200_OK)

        if request.user.is_authenticated:
            data["first_name"] = request.user.first_name
            data["last_name"] = request.user.last_name
            data["email"] = request.user.email
            data["is_superuser"] = request.user.is_superuser
            return Response(data, status=status.HTTP_200_OK)

        # pylint: disable=line-too-long
        return Response(SSO_SERVICE_APP_URL, status=status.HTTP_302_FOUND)  # type: ignore[unreachable]
