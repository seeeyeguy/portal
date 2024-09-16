"""
Cache module for wsgi requests. Caching
helps improve performance as we can store
computational expensive requests in the
cache for use later if we know that such
a request is unlikely to change often. We
would typically use this decorator on any
request that involved fetching data from the
API.
"""

import hashlib
from functools import wraps
from typing import Callable, cast, Union

from django.core.cache import cache
from django.http import HttpRequest, HttpResponseBase
from rest_framework import status

from manager.settings import CACHES

ACCEPTED_METHODS = ("POST", "GET")


def cache_request(timeout: int) -> Callable:
    """
    Decorator adapted for caching `POST` requests. Django's
    built-in `cache_page` decorator does not support
    `POST` requests, and although generally we would only
    cache a `GET` request due its idempotent nature, we
    occasionally use the `POST` request method to fetch
    data from the server when necessary.
    """

    def decorator(view_handler: Callable) -> Callable:
        @wraps(view_handler)
        def wrapper(
            request: HttpRequest, body: dict, *args: tuple, **kwargs: dict
        ) -> HttpResponseBase:
            if request.method not in ACCEPTED_METHODS:
                response: HttpResponseBase = view_handler(
                    request, body, *args, **kwargs
                )
                return response

            # Get path from request.
            full_path = request.get_full_path()

            # Use the path and request params to form a
            # unique key for the request.
            url_params = str(body).replace(" ", "")
            cache_key = hashlib.md5(
                f"{full_path}?params={url_params}".encode()
            ).hexdigest()

            # Check the cache for the response.
            response: Union[HttpResponseBase, None] = cache.get(key=cache_key)
            if response is None:
                # If the cached request does not exist,
                # make the call to the view and set the
                # cache with the response.
                response: HttpResponseBase = view_handler(  # type: ignore[unreachable]
                    request, body, *args, **kwargs
                )
                if response.status_code == status.HTTP_200_OK:
                    cache.set(
                        key=cache_key,
                        value=response,
                        timeout=timeout,
                    )
            return response

        return wrapper

    return decorator


DEFAULT_TIMEOUT = cast(int, CACHES["default"]["TIMEOUT"])
