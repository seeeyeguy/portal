""" Generic view decorators for view routes. """

import json
import logging
from functools import wraps
from typing import Any, Callable, Type, Union

from django import http
from rest_framework import status
from rest_framework.serializers import Serializer

LOGGER = logging.getLogger(__name__)


def with_serializer(serializer_class: Type[Serializer], many: bool = False) -> Callable:
    """Coerce the HTTP POST body or GET params into a form specified
    via `serializer_class`. The body becomes available as the second
    parameter to the view function as an OrderedDict containing keys
    from the serializer. This decorator should appear last in the
    decorator chain."""

    def decorator(view_handler: Callable) -> Callable:
        @wraps(view_handler)
        def wrapper(
            request: http.HttpRequest, *args: object, **kwargs: dict
        ) -> Union[http.JsonResponse, Any]:

            # Parse the body. If request.body is empty, e.g. b'', instead provide an
            # empty dict for json.loads to parse.
            body = json.loads(request.body or b"{}")
            # Parse the params, if GET request.
            if request.method in {"GET", "DELETE"}:
                body = request.GET
            req = serializer_class(data=body, many=many)

            # Verify the parameters.
            if not req.is_valid():
                LOGGER.debug(f"Invalid request: {str(req.errors)}")
                return http.JsonResponse(
                    req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
                )
            return view_handler(request, req.validated_data, *args, **kwargs)

        return wrapper

    return decorator


def login_required() -> Callable:
    """Decorator to check if a user is logged in before
    executing the view. This decorator ensures the user making
    the request is logged in by checking the is_authenticated
    field for the user. If the user is not logged in this decorator
    returns a JsonResponse with a 401 Unauthorized status code."""

    def decorator(view_handler: Callable) -> Callable:
        @wraps(view_handler)
        def wrapper(
            request: http.HttpRequest, *args: object, **kwargs: dict
        ) -> Union[http.JsonResponse, Any]:
            if not request.user.is_authenticated:
                err_msg: str = "Not authorized to access resource."
                LOGGER.error(err_msg)
                return http.JsonResponse(
                    err_msg, status=status.HTTP_401_UNAUTHORIZED, safe=False
                )

            return view_handler(request, *args, **kwargs)

        return wrapper

    return decorator


def admin_required() -> Callable:
    """Decorator to check if a user has superuser privileges
    before executing the view. This decorator ensures the user
    making the request has superuser privileges by checking the
    is_superuser field for the user. If the user does not have
    superuser privileges this decorator returns a JsonResponse
    with a 403 Forbidden status code."""

    def decorator(view_handler: Callable) -> Callable:
        @wraps(view_handler)
        def wrapper(
            request: http.HttpRequest, *args: object, **kwargs: dict
        ) -> Union[http.JsonResponse, Any]:
            if not request.user.is_superuser:
                err_msg: str = "Permissions Denied."
                LOGGER.error(err_msg)
                return http.JsonResponse(
                    err_msg, status=status.HTTP_403_FORBIDDEN, safe=False
                )

            return view_handler(request, *args, **kwargs)

        return wrapper

    return decorator
