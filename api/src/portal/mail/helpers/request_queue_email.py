"""
Queue email reminders for pending requests.
"""

import logging

import django_rq
from django.template.loader import render_to_string

from portal.mail.helpers.base import (
    create_base_template_context_for_email,
    generate_html_message_for_email,
    send_email,
)
from portal.mail.helpers.request_email_helpers import (
    find_admins_with_pending_requests,
    get_pending_request_summary,
    get_request_status_change_details,
    get_stage_display,
    get_weekly_summary_for_superuser,
)
from request.models.Request import Request
from request.models.Stage.Stage import Stage
from users.models import Access, Role


LOGGER = logging.getLogger(__name__)


def queue_admin_reminder_emails() -> None:
    """
    Queues reminder emails for admins with pending requests to review.

    Accepts:
        * None

    Returns:
        * None
    """
    admins_requests = find_admins_with_pending_requests()

    if not admins_requests:
        LOGGER.info("No pending requests found for admins to review.")
        return

    LOGGER.info(f"Queueing reminder emails for {len(admins_requests)} admin(s).")

    for admin, requests_list in admins_requests.items():
        try:
            recipients = [admin.user.email]

            # Prepare context for template
            context = {
                "admin_first_name": admin.user.first_name.capitalize(),
                "request_count": len(requests_list),
                "requests": requests_list,
            }

            # Render the HTML template
            html_content = render_to_string(
                "request_reminders.html",
                {"email_type": "admin_reminder", **context},
            )

            context = create_base_template_context_for_email(
                html_content,
                app_name="BI Portal",
            )
            html_message = generate_html_message_for_email(context)
            subject = (
                f"Action Required: {len(requests_list)} pending request(s) to review"
            )

            django_rq.enqueue(send_email, recipients, None, html_message, subject)
            LOGGER.info(f"Queued reminder email for admin {admin.user.email}")

        except Exception as exc:
            LOGGER.error(f"Failed to queue email for admin {admin.user.email}: {exc}")


def queue_superuser_weekly_summary_emails() -> None:
    """
    Queues weekly summary emails for all superusers.

    This function generates a comprehensive weekly report showing:
    - Total pending requests (excluding DRAFT)
    - Count of requests awaiting BPE review
    - Count of requests awaiting Superuser approval
    - Requests grouped by SubFunction in a consolidated table
    - Days pending in current stage for each request (color-coded)
    - Available BPE reviewers for each SubFunction
    - Warning for SubFunctions without BPE reviewers
    - Function (SubFunction) format for better organization
    - User-friendly stage names (e.g., "Awaiting BPE Review", "Awaiting SU Approval")

    Accepts:
        * None

    Returns:
        * None
    """
    # Get summary data
    summary_data = get_weekly_summary_for_superuser()

    if summary_data["total_pending"] == 0:
        LOGGER.info(
            "No pending requests for weekly summary. Skipping superuser emails."
        )
        return

    # Get all superuser accesses
    superuser_accesses = (
        Access.objects.filter(
            role__level=Role.RoleLevels.SUPERUSER,
            access_revoked_date__isnull=True,
        )
        .select_related("user", "role")
        .distinct()
    )

    if not superuser_accesses.exists():
        LOGGER.info("No active superusers found for weekly summary.")
        return

    LOGGER.info(
        f"Queueing weekly summary emails for {superuser_accesses.count()} superuser(s)."
    )

    for access in superuser_accesses:
        try:
            recipients = [access.user.email]

            # Find SubFunctions without BPE reviewers
            subfunctions_without_bpe = []
            for subfunction_name, data in summary_data["by_subfunction"].items():
                if not data["bpe_reviewers"]:
                    subfunctions_without_bpe.append(subfunction_name)

            # Prepare all requests data for template
            all_requests = []
            for subfunction_name, data in summary_data["by_subfunction"].items():
                # Format BPE reviewers list (names only)
                bpe_reviewers = (
                    [bpe["name"] for bpe in data["bpe_reviewers"]]
                    if data["bpe_reviewers"]
                    else []
                )

                # Get Function name for this SubFunction
                function_name = data.get("function_name", "Unknown")

                for req in data["requests"]:
                    all_requests.append(
                        {
                            "id": req["id"],
                            "name": req["name"],
                            "subfunction": subfunction_name,
                            "function_name": function_name,
                            "days_pending": req["days_pending"],
                            "stage": req["stage"],
                            "stage_display": get_stage_display(
                                req["current_stage_level"]
                            ),
                            "originator": req["originator"],
                            "bpe_reviewers": bpe_reviewers,
                        }
                    )

            # Sort by days pending (oldest first)
            all_requests.sort(key=lambda x: x["days_pending"], reverse=True)

            # Prepare context for template
            context = {
                "superuser_first_name": access.user.first_name.capitalize(),
                "total_pending": summary_data["total_pending"],
                "oldest_days_pending": summary_data["oldest_days_pending"],
                "awaiting_bpe_count": summary_data.get("awaiting_bpe_count", 0),
                "awaiting_su_count": summary_data.get("awaiting_su_count", 0),
                "subfunctions_without_bpe": subfunctions_without_bpe,
                "all_requests": all_requests,
            }

            # Render the HTML template
            html_content = render_to_string(
                "request_reminders.html",
                {"email_type": "superuser_weekly_summary", **context},
            )

            context = create_base_template_context_for_email(
                html_content, app_name="BI Portal"
            )
            html_message = generate_html_message_for_email(context)
            subject = f"Weekly Summary: {summary_data['total_pending']} Pending Request(s) - Action Required"

            django_rq.enqueue(send_email, recipients, None, html_message, subject)
            LOGGER.info(
                f"Queued weekly summary email for superuser {access.user.email}"
            )

        except Exception as exc:
            LOGGER.error(
                f"Failed to queue weekly summary for {access.user.email}: {exc}"
            )


def queue_originator_status_change_email(request: Request, status_type: str) -> None:
    """
    Queues an email to the originator when their request status changes.

    This function notifies the request originator about status changes:
    - Approved: The request has been approved
    - Rejected: The request has been denied by a reviewer
    - Revised: The request needs modifications before it can be approved

    The email includes:
    - Request details (ID, resource name, current stage)
    - Reviewer information (who made the decision)
    - Reviewer comments explaining the decision
    - Next steps for the originator (if applicable)

    Accepts:
        * request (Request): The request that had a status change.
        * status_type (str): Type of status change - 'approved', 'rejected', or 'revised'.

    Returns:
        * None
    """
    if status_type not in ["approved", "rejected", "revised"]:
        resource_name = getattr(getattr(request, "resource", None), "name", "Unknown")
        LOGGER.error(
            f"Invalid status_type: {status_type} for Request #{request.id} "
            f"({resource_name}). Must be 'approved', 'rejected', or 'revised'."
        )
        return

    try:
        # Get request details
        details = get_request_status_change_details(request)

        if not details:
            LOGGER.error(
                f"Could not get details for request {request.id}. "
                f"Skipping {status_type} notification email."
            )
            return

        recipients = [details["originator_email"]]

        # Prepare context for template
        context = {
            "originator_first_name": request.originator.user.first_name.capitalize(),
            "request_id": details["request_id"],
            "resource_name": details["resource_name"],
            "stage_display": details["stage_display"],
            "reviewer_name": details["reviewer_name"],
            "reviewer_comments": details["reviewer_comments"],
            "transition_date": details["transition_date"],
            "status_type": status_type,
        }

        # Render the HTML template
        html_content = render_to_string(
            "request_reminders.html",
            {"email_type": f"originator_{status_type}", **context},
        )

        context = create_base_template_context_for_email(
            html_content,
            app_name="BI Portal",
        )
        html_message = generate_html_message_for_email(context)

        # Set subject based on status type
        if status_type == "approved":
            subject = f"Request #{details['request_id']} - {details['resource_name']} has been approved"
        elif status_type == "rejected":
            subject = f"Request #{details['request_id']} - {details['resource_name']} has been rejected"
        else:  # revised
            subject = f"Request #{details['request_id']} - {details['resource_name']} requires revisions"

        django_rq.enqueue(send_email, recipients, None, html_message, subject)
        LOGGER.info(
            f"Queued {status_type} notification email for originator {details['originator_email']} "
            f"(Request #{details['request_id']})"
        )

    except Exception as exc:
        LOGGER.error(
            f"Failed to queue {status_type} email for request {request.id}: {exc}"
        )


def check_and_queue_request_emails() -> None:
    """
    Main function to check for pending requests and queue appropriate reminder emails.
    This function is called by the cron job.

    Sends emails to:
        - Admins - reminding them to review pending requests

    Accepts:
        * None

    Returns:
        * None
    """
    try:
        summary = get_pending_request_summary()
        LOGGER.info(f"Checking pending requests: {summary['total_pending']} total")

        if summary["total_pending"] == 0:
            LOGGER.info("No pending requests found. Skipping email reminders.")
            return

        # Queue emails for admins (people who need to approve requests)
        queue_admin_reminder_emails()

        LOGGER.info("Successfully queued all request reminder emails.")

    except Exception as exc:
        LOGGER.error(f"Error in check_and_queue_request_emails: {exc}")
