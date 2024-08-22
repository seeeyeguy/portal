""" 
BI Portal `Analytics` apps module. Using AnalyticsConfig.ready(),
we can configure our app here with data or processes on init.
"""


from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    """App Config for `Analytics` app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "analytics"
