"""
`Program Review Tool` apps module. Using ProgramReviewToolConfig.ready(),
we can config our app here with data or processes on init.
"""

from django.apps import AppConfig


class ProgramReviewToolConfig(AppConfig):
    """App Config for `ProgramReviewTool` app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "program_review_tool"
