"""
Context processors to inject data into the
context of Django templates. These context
processors accept a Django.http.HttpRequest
and return a dictionary of data that is merged
with a template's context.
"""

from django.http import HttpRequest

from manager import settings


def app(request: HttpRequest) -> dict:
    """Context processor that provides application data
    to the template context."""

    return {
        "app_name": settings.APP_NAME,
        "build": settings.BUILD,
        "company_name": "L3Harris Technologies.",
    }
