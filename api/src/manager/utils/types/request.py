"""
Type module for request. This module provides
custom types for a request. Sometimes, a type
may not exist that accurately describes our
variables, parameters, or returns and so
we must create our own and place them here.
"""

from django.contrib.auth import models
from django.http import HttpRequest


class DjangoHttpRequest(HttpRequest):
    """Type annotation for Django HttpRequest."""

    user: models.User
