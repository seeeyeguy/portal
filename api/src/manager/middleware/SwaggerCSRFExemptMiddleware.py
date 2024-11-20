"""
Middleware module providing CSRF tokens to Swagger UI requests,
if and only if the application is in a `development` environment.
SwaggerCSRFExemptMiddleware makes it easier for a developer
to make requests through the Swagger UI, allowing them to ensure
the API's functionality. The middleware will take the request, and 
will leverage Django's built-in django.middleware.csrf.get_token function
to generate a new CSRF token and assign it to the request's cookies and 
headers.
"""

from typing import Callable

from django import conf, http
from django.middleware.csrf import get_token

from manager import settings
from manager.utils.types.request import DjangoHttpRequest


class SwaggerCSRFExemptMiddleware:
    """Middleware to add CSRF token to request, specifically for the
    Swagger UI when the application is in a `development`
    environment."""

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: DjangoHttpRequest) -> http.HttpResponseBase:

        self.add_csrf_token(request=request)
        response: http.HttpResponseBase = self.get_response(request)

        return response

    def add_csrf_token(self, request: DjangoHttpRequest) -> None:
        """
        If and only if the application is in a `development`
        environment, add CSRF token to the request, to allow
        Swagger UI to submit POST, PUT & DELETE requests.

        Accepts:
            request (DjangoHttpRequest): An http request from the client.

        Returns:
            * None
        """

        if (
            settings.BUILD != settings.ApplicationBuild.DEVELOPMENT
            or request.headers["Origin"].lower() != settings.SWAGGER_APP_ORIGIN.lower()
        ):
            return None

        # Generate CSRF token for request.
        csrf_token = get_token(request=request)

        # Add CSRF token to request cookies.
        request.COOKIES[conf.settings.CSRF_COOKIE_NAME] = csrf_token

        # Assign CSRF token to the request's META.
        request.META.update({conf.settings.CSRF_HEADER_NAME: csrf_token})

        return None
