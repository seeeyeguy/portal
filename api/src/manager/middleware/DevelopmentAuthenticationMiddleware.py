"""
Middleware module providing authentication to developers, if and only
if the application is in a `development` or `test` environment.
DevelopmentAuthenticationMiddleware makes it easy for a developer
to login as a custom user, even if that user does not exist. The
middleware will login a custom user specified in a developer's .env with
the environment variables `SSO_DEVELOPMENT_USER_FIRST_NAME` and
`SSO_DEVELOPMENT_USER_LAST_NAME`. A developer can even have more granular
control of authentication by instantiating the request headers with 
`SSO_DEVELOPMENT_USER_REQUEST_HEADERS_KEY`. This makes it easier to test
the application's functionality where authentication would be required.
"""

import json
import logging
from typing import Callable

from django import http
from django.contrib.auth import get_user_model, login

from manager import settings
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)

User = get_user_model()


class DevelopmentAuthenticationMiddleware:
    """Middleware to login a user, specified by the developer when the
    application is in a `development` environment."""

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: DjangoHttpRequest) -> http.HttpResponseBase:
        # Login development user, if and only if BUILD==development.
        self.login_dev_user(request=request)

        response: http.HttpResponseBase = self.get_response(request)

        return response

    def login_dev_user(self, request: DjangoHttpRequest) -> None:
        """
        If and only if the application is in a `development`, or `test`
        environment, login the user specified by the developer.

        Accepts:
            request (DjangoHttpRequest): An http request from the client.

        Returns:
            * None
        """

        if settings.BUILD not in (
            settings.ApplicationBuild.DEVELOPMENT,
            settings.ApplicationBuild.TEST,
        ):
            return None

        email = (
            f"{settings.SSO_DEVELOPMENT_USER['first_name']}"
            f".{settings.SSO_DEVELOPMENT_USER['last_name']}@l3harris.com"
        )
        if settings.SSO_DEVELOPMENT_USER_REQUEST_HEADERS_KEY in request.headers:
            try:
                dev_user_from_request = json.loads(
                    request.headers[settings.SSO_DEVELOPMENT_USER_REQUEST_HEADERS_KEY]
                )
                first_name = dev_user_from_request["first_name"]
                last_name = dev_user_from_request["last_name"]
                email = dev_user_from_request["email"]

                if not User.objects.filter(email=email).exists():
                    User.objects.create(
                        username=email,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                    )
            except (json.decoder.JSONDecodeError, KeyError):
                pass  # fail silently, login dev user.

        try:
            development_user = User.objects.get(email=email)
            login(request=request, user=development_user)
            return None
        except User.DoesNotExist:
            LOGGER.error("Development login failed! Development user does not exist.")
            return None
