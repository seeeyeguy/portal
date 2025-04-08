"""
Config module to configure settings to connect to
the application's database. Several database settings
may be specified here, including `BASE`, `TEST`, and
more.
"""

import os

# pylint: disable=too-few-public-methods


## Internal Databases.
class BASE:
    """Base Database Settings."""

    ENGINE = "django.db.backends.postgresql_psycopg2"
    NAME = os.getenv("POSTGRES_NAME", "django_app")
    USER = os.getenv("POSTGRES_USER", "postgres")
    PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    HOST = os.getenv("POSTGRES_HOST", "database")
    PORT = os.getenv("POSTGRES_PORT", "5432")
    TEST = {"NAME": "test_default"}
    ATOMIC = os.getenv("POSTGRES_ATOMIC_REQUESTS", "True").title() == "True"


class PROGRAM_REVIEW_TOOL(BASE):  # pylint: disable=invalid-name
    """Program Review Tool Database Settings."""

    NAME = os.getenv("POSTGRES_PROGRAM_REVIEW_TOOL_NAME", "django_app")
    USER = os.getenv("POSTGRES_PROGRAM_REVIEW_TOOL_USER", "postgres")
    PASSWORD = os.getenv("POSTGRES_PROGRAM_REVIEW_TOOL_PASSWORD", "postgres")
    TEST = {"NAME": "test_prt"}


## External Databases.
class AXIS:
    """AXIS Database Settings."""

    NAME = os.getenv("AXIS_DATABASE_NAME", "axis")
    USER = os.getenv("AXIS_DATABASE_USER", "SA")
    PASSWORD = os.getenv("AXIS_DATABASE_PASSWORD", "mssql")
    HOST = os.getenv("AXIS_DATABASE_HOST", "axis")
    PORT = os.getenv("AXIS_DATABASE_PORT", "1433")


class FDW:
    """FDW Database Settings."""

    NAME = os.getenv("FDW_DATABASE_NAME", "django_app")
    USER = os.getenv("FDW_DATABASE_USER", "oracle12")
    PASSWORD = os.getenv("FDW_DATABASE_PASSWORD", "oracle12")
    HOST = os.getenv("FDW_DATABASE_HOST", "fdw")
    PORT = os.getenv("FDW_DATABASE_PORT", "1521")


class TEST:
    """Test Database Settings."""

    ENGINE = "django.db.backends.postgresql_psycopg2"
    NAME = "test.db"


EXTERNAL_SOURCE_DATABASE = os.getenv("EXTERNAL_SOURCE_DATABASE", "axis")
