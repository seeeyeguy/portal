"""
Config module to configure settings to connect to
the application's cache(s). Several cache settings
may be specified here, including `CACHE`, `CHANNEL`,
`TASKQUEUE`, and more. `CACHE` is used to cache
wsgi requests. `CHANNEL` is used to help provide
communication using an asgi server between all
client members of a group listening on a websocket.
`TASKQUEUE` is used to store jobs to be executed by
workers (RQ, Celery).
"""

import os

# pylint: disable=too-few-public-methods


class CACHE:
    """Application Cache Settings."""

    BACKEND = "django_redis.cache.RedisCache"
    PASSWORD = os.getenv("REDIS_CACHE_PASSWORD", "password")
    HOST = os.getenv("REDIS_CACHE_HOST", "cache")
    PORT = os.getenv("REDIS_CACHE_PORT", "6379")


class CHANNEL:
    """Application Websocket Channel Settings."""

    BACKEND = "channels_redis.core.RedisChannelLayer"
    PASSWORD = os.getenv("REDIS_CHANNEL_PASSWORD", "password")
    HOST = os.getenv("REDIS_CHANNEL_HOST", "channel")
    PORT = os.getenv("REDIS_CHANNEL_PORT", "6379")


class TASKQUEUE:
    """Application Task Queue Settings."""

    PASSWORD = os.getenv("REDIS_TASKQUEUE_PASSWORD", CACHE.PASSWORD)
    HOST = os.getenv("REDIS_TASKQUEUE_HOST", "queue")
    PORT = os.getenv("REDIS_TASKQUEUE_PORT", CACHE.PORT)
