"""
Config module to configure settings to connect to
the application's database. Several database settings
may be specified here, including `BASE`, `TEST`, and
more.
"""

import os

# pylint: disable=too-few-public-methods


class BASE:
    """Base Database Settings."""

    ENGINE = "django.db.backends.postgresql_psycopg2"
    NAME = os.getenv("POSTGRES_NAME", "django_app")
    USER = os.getenv("POSTGRES_USER", "postgres")
    PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    HOST = os.getenv("POSTGRES_HOST", "database")
    PORT = os.getenv("POSTGRES_PORT", "5432")
    TEST = {"NAME": "test_django"}
    ATOMIC = os.getenv("POSTGRES_ATOMIC_REQUESTS", "True").title() == "True"


class TEST:
    """Test Database Settings."""

    ENGINE = "django.db.backends.sqlite3"
    NAME = "test.db"
