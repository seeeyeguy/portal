""" 
BI Portal `Preferences` apps module. Using PreferencesConfig.ready(),
we can config our app here with data or processes on init.
"""

from django.apps import AppConfig


class PreferencesConfig(AppConfig):
    """App Config for `Preferences` app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "preferences"
