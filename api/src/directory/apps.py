""" 
BI Portal `Directory` apps module. Using DirectoryConfig.ready(),
we can config our app here with data or processes on init.
"""

from django.apps import AppConfig


class DirectoryConfig(AppConfig):
    """App Config for `Directory` app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "directory"
