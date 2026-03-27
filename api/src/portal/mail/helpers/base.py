import logging
import os
from jinja2 import Environment, FileSystemLoader
from typing import Any, List

from django.core.mail import send_mail

from manager import settings

# Load template directory for mail module.
TEMPLATE_DIR = os.path.join(settings.BASE_DIR, "portal/mail/templates/")
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
LOGGER = logging.getLogger(__name__)


def create_base_template_context_for_email(
    email_message: str,
    url: str = "",
    app_name: str = settings.APP_NAME,
    application_contact: str = settings.DEFAULT_FROM_EMAIL,
) -> dict[str, Any]:
    """
    Create a context to populate the html email message.

    Accepts:
        * email_message (str): The textual content of the email.
        * url (str): A link that the recipient may click.
        * app_name (str): The name of the application.
        * application_contact (str): The contact email for an admin
            of the application.

    Returns:
        * (dict): Context data to render the email template.
    """

    return {
        "email_message": email_message,
        "url": url,
        "app_name": app_name,
        "from_email": application_contact,
    }


def generate_html_message_for_email(
    context: dict, template_name: str = "base_email.html"
) -> str:
    """
    Create a text/html notification message.

    Accepts:
        * context (dict): Context data to render the email template.
        * template_name (str): Template name to render.

    Returns:
        * (Jinja2.Template(str)): A rendered template for an email message.
    """

    template = env.get_template(template_name)
    return template.render(context)


def send_email(
    recipients: List[str],
    message: str,
    html_message: str,
    subject: str,
    from_email: str = settings.DEFAULT_FROM_EMAIL,
) -> None:
    """
    Send an automated email to a collection of recipients.

    Accepts:
        * recipients (list): A list of email contacts to send this email to.
        * message (str): Plain text body of the email.
        * html_message (str): A rendered Jinja2 template.
        * subject (str): A subject for the email.
        * from_email (str): The contact email for the sender.

    Returns:
        * None
    """

    if settings.BUILD == settings.ApplicationBuild.PRODUCTION:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipients,
            html_message=html_message,
        )
    else:
        log_msg = (
                f"Subject({subject})"
                f" Recipients({recipients})"
                f" Message={message}"
            )
        LOGGER.info(log_msg)