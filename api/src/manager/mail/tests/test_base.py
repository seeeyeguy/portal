"""
Test module to test basic email functionality.
"""

import django_rq

from django.test import TestCase

from manager.mail.helpers.base import (
    create_base_template_context_for_email,
    generate_html_message_for_email,
    send_email,
)
from manager.settings import APP_NAME


class TestMail(TestCase):
    """Test suite for manager.mail module (emails)."""

    def _send_email(self, email_message: str, recipients: list) -> None:
        """Helper function to send an email."""

        context = create_base_template_context_for_email(email_message=email_message)
        html = generate_html_message_for_email(context=context)
        send_email(
            recipients=recipients,
            message=email_message,
            html_message=html,
            subject=f"{APP_NAME} Test!",
        )

    def test_connection(self) -> None:
        """Success Case: Ensure connection to task queue."""

        queue = django_rq.get_queue("default")
        self.assertIsNotNone(queue.connection)
