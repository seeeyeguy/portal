"""
Middleware module provides the appropriate `User` for the
request, given the path on that request. Considering we
are managing an application with multiple databases, we must
ensure that we are providing the appropriate `User` for the
appropriate application, else we may experience data integrity
issues. `MultiDatabaseRequestUserMiddleware` will modify the
`User` on the request by injecting request.user whilst the
request is in-flight, if and only if, the path of the request
corresponds to an application outside of the `default` application.
"""

# pylint: disable=wrong-import-order
from asgiref.sync import sync_to_async
from functools import partial
from typing import Callable, cast

from django import http
from django.contrib.auth import models as AuthModels

from manager.utils.types.request import DjangoHttpRequest


async def async_program_review_tool_user(request):  # type: ignore[no-untyped-def]
    """Fetch the `User` on the given request asynchronously."""

    def program_review_tool_user():  # type: ignore[no-untyped-def]
        return request.user

    return await sync_to_async(program_review_tool_user)  # type: ignore[misc]


class MultiDatabaseRequestUserMiddleware:
    """Middleware to potentially inject a `User` into the request, given
    the path of the request."""

    PROGRAM_REVIEW_TOOL_APPLICATION_NAME: str = "program-review-tool"
    PROGRAM_REVIEW_TOOL_DATABASE_ALIAS: str = "prt"

    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: DjangoHttpRequest) -> http.HttpResponseBase:
        """Method to allow a class to be a `Callable`."""

        url_path: str = request.get_full_path()

        if self.PROGRAM_REVIEW_TOOL_APPLICATION_NAME in url_path:
            user = request.user
            if user.is_authenticated:
                prt_user: AuthModels.User = cast(
                    AuthModels.User,
                    (
                        AuthModels.User.objects.using(
                            self.PROGRAM_REVIEW_TOOL_DATABASE_ALIAS
                        )
                        .filter(username=user.username)
                        .first()
                    ),
                )

                request.user = prt_user

                request.auser = partial(
                    async_program_review_tool_user, request
                )  # type: ignore[assignment]

        response: http.HttpResponseBase = self.get_response(request)

        return response
