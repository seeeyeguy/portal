""" Generic view decorators for view routes. """

import json
import logging
from functools import wraps
from typing import Any, Callable, Type, Union

from django import http
from rest_framework import status
from rest_framework.serializers import Serializer

LOGGER = logging.getLogger(__name__)


def with_serializer(serializer_class: Type[Serializer]) -> Callable:
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
            if request.method == "GET":
                body = request.GET
            req = serializer_class(data=body)

            # Verify the parameters.
            if not req.is_valid():
                LOGGER.debug(f"Invalid request: {str(req.errors)}")
                return http.JsonResponse(req.errors, status=status.HTTP_400_BAD_REQUEST)
            return view_handler(request, req.validated_data, *args, **kwargs)

        return wrapper

    return decorator
