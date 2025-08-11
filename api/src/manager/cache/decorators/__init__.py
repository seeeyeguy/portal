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

            # Construct the cache key prefix from the request's path
            # (i.e. /v1/diretory/tag) excluding the '/search' suffix.
            # Note: The query params are not part of the path. This
            # key prefix is used as the marker to search and delete
            # associated cache entries (i.e. header & cache_page).
            cache_key_prefix = md5(
                request.build_absolute_uri(request.path.removesuffix("/search")).encode(
                    "ascii"
                ),
                usedforsecurity=False,
            ).hexdigest()

            request_cache_key = xxhash.xxh64(
                f"{full_path}?params={url_params}".encode()
            ).hexdigest()

            # Construct the cache key suffix from the request's full
            # path (i.e /v1/directory/tag/search?label=a). Note: The
            # query params are taken into account for this hash. This
            # key suffix is used as the marker to search and delete
            # associated cache entries for 'search' requests as each
            # search will have a hash that is dependent on the request's
            # full path.
            cache_key_suffix = md5(
                request.build_absolute_uri(full_path).encode("ascii"),
                usedforsecurity=False,
            ).hexdigest()

            cache_key = f"{cache_key_prefix}_{request_cache_key}_{cache_key_suffix}"

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
                # Construct the md5 hash from the request's path, which is the
                # cache key's prefix.
                cache_key_prefix = md5(
                    request.build_absolute_uri(request.path).encode("ascii"),
                    usedforsecurity=False,
                ).hexdigest()

                # We want to query all the cache keys for the same request path
                # using the prefix key. Each hash key for each related request path will
                # have this prefix key and a distinct suffix key. We can use these hashes
                # to get the associated suffix keys, which encompass the query params of
                # their request. This is important because endpoints such as 'search' have
                # frequently changing query params (i.e. frequently changing hashes), and
                # so we need the prefix key to group all the suffix keys.
                cache_key_suffixes = [
                    key.split("_")[-1]
                    for key in cache.keys(f"*{cache_key_prefix}*")  # type: ignore[attr-defined]
                    if "views." not in key
                ]

                # Delete cache entries that match
                # the cache_key_prefix.
                cache.delete_pattern(f"*{cache_key_prefix}*")  # type: ignore[attr-defined]

                # Loop through the cache key suffixes and delete any
                # matching entries.
                for cache_key_suffix in cache_key_suffixes:
                    cache.delete_pattern(f"*{cache_key_suffix}*")  # type: ignore[attr-defined]
            return response

        return wrapper

    return decorator


DEFAULT_TIMEOUT = cast(int, CACHES["default"]["TIMEOUT"])
