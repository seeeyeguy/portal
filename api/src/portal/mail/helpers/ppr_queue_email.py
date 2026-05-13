import django_rq
from typing import List, Tuple

from portal.mail.helpers.base import (
    create_base_template_context_for_email,
    generate_html_message_for_email,
    send_email,
)
from .ppr_email_helpers import days_until_next_month, find_members_programs, is_overdue

REMINDER_DAYS = {1, 2, 5, 10}


def format_message(member: str, overdue: List) -> str:
    """
    Generates the reminder email string

    Accepts:
        * member (str): Name of the member the email is addressed to
        * overdue (list): A list containing:
            - (bool): whether today is past due
            - (list: [int, int]): current reporting period year, month
            - (str): month of the due date

    Returns:
        * message (str): The reminder email message.
    """

    due = f"by {overdue[2]} 1"
    if overdue[0]:
        due = "as soon as possible"
    message = (
        f"Hello {member}, \n\n"
        f"This is a reminder to complete your Program Performance Reporting for Period "
        f"{overdue[1][1]} FY{overdue[1][0]}. If you have not yet submitted your report, please "
        f"do so {due} using the following link: https://theportal.l3harris.com/ppr\n\n"
        "CHQ requires all Tier 1/2 programs to report financial performance and provide "
        "subjective assessments of key program areas. Available data has been pre-populated; any "
        "remaining fields require manual entry. Additional details for each may be accessed via "
        "the tooltips within the application.\n\n"
        "Red Programs / Return-To-Green Plans\n"
        'Programs identified as "red" must document their return-to-green plans as actionable '
        "tasks in the designated section at the bottom of the tool. This should align with your "
        "standard task reporting approach."
    )

    return message


def format_html_message(member: str, overdue: List) -> str:
    """
    Generates the reminder email html as a string

    Accepts:
        * member (str): Name of the member the email is addressed to
        * overdue (list): A list containing:
            - (bool): whether today is past due
            - (list: [int, int]): current reporting period year, month
            - (str): month of the due date

    Returns:
        * message (str): The reminder html email message.
    """

    due = f"by <b>{overdue[2]} 1</b>"
    if overdue[0]:
        due = "<b>as soon as possible</b>"
    message = (
        f"Hello {member}, <br><br>"
        f"This is a reminder to complete your <b>Program Performance Reporting for Period "
        f"{overdue[1][1]} FY{overdue[1][0]}</b>. If you have not yet submitted your report, please "
        f"do so {due} using the following link: https://theportal.l3harris.com/ppr<br><br>"
        "CHQ requires all Tier 1/2 programs to report financial performance and provide "
        "subjective assessments of key program areas. Available data has been pre-populated; any "
        "remaining fields require manual entry. Additional details for each may be accessed via "
        "the tooltips within the application.<br><br>"
        "<b>Red Programs / Return-To-Green Plans</b> <br>"
        'Programs identified as "red" must document their return-to-green plans as actionable '
        "tasks in the designated section at the bottom of the tool. This should align with your "
        "standard task reporting approach."
    )

    return message


def check_and_queue_email() -> None:
    """
    Queues a PPR reminder email on set days before the due date, or if overdue.

    Accepts:
        * None

    Returns:
        * None
    """

    days = days_until_next_month()
    overdue = is_overdue()
    if days in REMINDER_DAYS or overdue[0]:
        members_programs = find_members_programs()
        for member in members_programs:
            recipients = [member.email]
            message = format_message(member.first_name, overdue)
            context = create_base_template_context_for_email(
                format_html_message(member.first_name, overdue)
            )
            html_message = generate_html_message_for_email(context, "ppr_reminder.html")
            subject = f"Period {overdue[1][1]} FY{overdue[1][0]} Program Performance Reporting Reminder"
            django_rq.enqueue(send_email, recipients, message, html_message, subject)