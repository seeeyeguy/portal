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

import xxhash
from functools import wraps
from hashlib import md5
from typing import Callable, cast, Union

from django.conf import settings
from django.core.cache import cache
from django.http import HttpRequest, HttpResponseBase
from django.utils.cache import get_cache_key
from rest_framework import status

from manager.settings import ApplicationBuild, CACHES

ACCEPTED_METHODS = ("POST", "GET")

ACCEPTED_MUTATION_METHODS = {"POST", "PUT", "DELETE"}


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
            if (
                request.method not in ACCEPTED_METHODS
                or settings.BUILD == ApplicationBuild.TEST
            ):
                response: HttpResponseBase = view_handler(
                    request, body, *args, **kwargs
                )
                return response

            # Get path from request.
            full_path = request.get_full_path()

            # Use the path and request params to form a
            # unique key for the request.
            url_params = str(body).replace(" ", "")
            md5_hash = md5(
                request.build_absolute_uri(request.path).encode("ascii"),
                usedforsecurity=False,
            ).hexdigest()
            xxh64_hash = xxhash.xxh64(
                f"{full_path}?params={url_params}".encode()
            ).hexdigest()

            cache_key = f"{md5_hash}_{xxh64_hash}"

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


def invalidate_request_cache() -> Callable:
    """
    Decorator that invalidates the `GET` request
    entries for an application resource. This decorator
    should be applied to `POST`, `PUT` & `DELETE`
    view methods.
    """

    def decorator(view_handler: Callable) -> Callable:
        @wraps(view_handler)
        def wrapper(
            request: HttpRequest, body: dict, *args: tuple, **kwargs: dict
        ) -> HttpResponseBase:

            response: HttpResponseBase = view_handler(request, body, *args, **kwargs)

            if (
                request.method not in ACCEPTED_MUTATION_METHODS
                or settings.BUILD == ApplicationBuild.TEST
            ):
                return response

            if response.status_code in {status.HTTP_200_OK, status.HTTP_201_CREATED}:
                # Construct the md5 hash from the request's path.
                request_md5_hash = md5(
                    request.build_absolute_uri(request.path).encode("ascii"),
                    usedforsecurity=False,
                ).hexdigest()
                # Delete cache entries that match
                # the md5 hash.
                cache.delete_pattern(f"*{request_md5_hash}*")  # type: ignore[attr-defined]
            return response

        return wrapper

    return decorator


DEFAULT_TIMEOUT = cast(int, CACHES["default"]["TIMEOUT"])
