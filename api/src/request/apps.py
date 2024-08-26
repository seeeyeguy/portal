""" 
BI Portal `Request` apps module. Using RequestConfig.ready(),
we can config our app here with data or processes on init.
"""

from django.apps import AppConfig


class RequestConfig(AppConfig):
    """App Config for `Request` app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "request"
