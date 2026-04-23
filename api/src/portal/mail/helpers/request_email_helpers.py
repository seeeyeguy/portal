"""
Helper functions for sending email reminders about pending requests.
"""

import logging
from typing import Any, Dict, List, Optional

from django.db.models import QuerySet
from django.utils import timezone

from directory.models.SubFunction import SubFunction
from request.models import Disposition
from request.models.Request import Request
from request.models.Stage.Stage import Stage
from request.models.Transition import Transition
from users.models import Access, Role


LOGGER = logging.getLogger(__name__)


def get_stage_display(stage_level: int) -> str:
    """
    Convert stage level to user-friendly display text.

    Accepts:
        * stage_level (int): The stage level integer value.

    Returns:
        * (str): User-friendly display text for the stage.
    """
    stage_map = {
        Stage.StageLevels.SUBMITTED: "Awaiting BPE Review",
        Stage.StageLevels.APPROVED_BY_BUSINESS_PROCESS_EXPERT: "Awaiting SU Approval",
        Stage.StageLevels.APPROVED_BY_SUPERUSER: "Approved",
        Stage.StageLevels.REJECTED_BY_BUSINESS_PROCESS_EXPERT: "Rejected by BPE",
        Stage.StageLevels.REJECTED_BY_SUPERUSER: "Rejected by SU",
        Stage.StageLevels.REVISE: "Revisions Requested",
        Stage.StageLevels.DRAFT: "Draft",
    }
    return stage_map.get(stage_level, "Unknown")


def find_pending_requests(days_pending: int = 0) -> QuerySet[Request]:
    """
    Fetches requests that are pending and need reminders.
    Excludes requests at DRAFT stage.

    Accepts:
        * days_pending (int): Minimum number of days a request must be pending
            to be included. Default is 0 (all pending requests).

    Returns:
        * pending_requests (QuerySet): Requests with PENDING status (excluding DRAFT).
    """
    pending_requests = Request.objects.filter(status=Request.RequestStatus.PENDING)

    # Exclude DRAFT stage requests by checking latest transition
    pending_request_ids = []
    for request in pending_requests:
        latest_transition = (
            Transition.objects.filter(request=request).order_by("-created").first()
        )

        # Only include if latest transition exists and is NOT at DRAFT stage
        if (
            latest_transition
            and latest_transition.stage.level != Stage.StageLevels.DRAFT
        ):
            pending_request_ids.append(request.id)

    # Filter to only include non-DRAFT requests
    pending_requests = pending_requests.filter(id__in=pending_request_ids)

    return pending_requests.select_related("resource", "originator", "originator__user")


def find_admins_with_pending_requests() -> Dict[Access, List[Request]]:
    """
    Creates a dictionary of admin users who need to review pending requests.

    Logic:
        - Business Process Experts: Get requests at SUBMITTED stage matching their assigned SubFunctions.
        - Super users: Get requests at APPROVED_BY_BUSINESS_PROCESS_EXPERT stage.

    The Access model has:
        - subfunctions (ManyToManyField): SubFunctions this Access can review.
        - stage (ManyToManyField): Stages at which this Access can submit Dispositions.

    The Resource model has:
        - subfunctions (ManyToManyField): SubFunctions this Resource belongs to.

    Accepts:
        * None

    Returns:
        * admin_to_requests (dict): Dictionary mapping Access objects to
            lists of pending Request objects they need to review.
            Format: {Access: [Request, Request, ...]}
    """
    pending_requests = find_pending_requests()

    if not pending_requests.exists():
        return {}

    admin_to_requests: Dict[Access, List[Request]] = {}

    # Get all active admin accesses (Superuser and Business Process Expert) to match with their pending requests
    admins = (
        Access.objects.filter(
            role__level__in=[
                Role.RoleLevels.SUPERUSER,
                Role.RoleLevels.BUSINESS_PROCESS_EXPERT,
            ],
            access_revoked_date__isnull=True,
        )
        .select_related("user", "role")
        .prefetch_related("subfunctions", "stage")
    )

    for admin in admins:
        user_requests: List[Request] = []

        for request in pending_requests:
            # Get the latest transition to determine current stage
            latest_transition = (
                Transition.objects.filter(request=request).order_by("-created").first()
            )

            if not latest_transition:
                continue

            current_stage = latest_transition.stage.level

            # Check if this Access is authorized to review at this stage
            authorized_stages = admin.stage.values_list("level", flat=True)

            if current_stage not in authorized_stages:
                continue

            # Super users: Only get reminders for requests awaiting their approval
            if admin.role.level == Role.RoleLevels.SUPERUSER:
                if (
                    current_stage
                    == Stage.StageLevels.APPROVED_BY_BUSINESS_PROCESS_EXPERT
                ):
                    user_requests.append(request)

            # Business Process Experts: Review requests at SUBMITTED stage, filtered by SubFunction
            elif admin.role.level == Role.RoleLevels.BUSINESS_PROCESS_EXPERT:
                if current_stage == Stage.StageLevels.SUBMITTED:
                    # Get SubFunctions this Access is authorized for
                    admin_subfunctions = set(
                        admin.subfunctions.values_list("id", flat=True)
                    )

                    # Get SubFunctions this Resource belongs to
                    resource_subfunctions = set(
                        request.resource.subfunctions.values_list("id", flat=True)
                    )

                    # Check if there's any overlap (Access can review this Resource)
                    if admin_subfunctions & resource_subfunctions:
                        user_requests.append(request)

        # Only add to dictionary if user has requests to review
        if user_requests:
            admin_to_requests[admin] = user_requests

    return admin_to_requests


def get_pending_request_summary() -> Dict[str, Any]:
    """
    Gets a summary of pending requests for reporting/logging purposes.

    Accepts:
        * None

    Returns:
        * summary (dict): Dictionary containing:
            - total_pending (int): Total number of pending requests.
            - oldest_request_date (datetime): Date of the oldest pending request.
    """
    pending_requests = find_pending_requests()

    if not pending_requests.exists():
        return {
            "total_pending": 0,
            "oldest_request_date": None,
        }

    oldest_request = pending_requests.order_by("created").first()

    return {
        "total_pending": pending_requests.count(),
        "oldest_request_date": oldest_request.created if oldest_request else None,
    }


def get_weekly_summary_for_superuser() -> Dict[str, Any]:
    """
    Generates a comprehensive weekly summary of all pending requests for superusers.

    This function provides a detailed breakdown of pending requests organized by SubFunction,
    including information about days pending in current stage, current stage, and available Business Process Expert reviewers.

    Excludes requests at DRAFT stage from all counts and summaries.

    Accepts:
        * None

    Returns:
        * summary (dict): Dictionary containing:
            - total_pending (int): Total number of pending requests (excluding DRAFT).
            - awaiting_bpe_count (int): Number of requests awaiting Business Process Expert review.
            - awaiting_su_count (int): Number of requests awaiting Superuser approval.
            - by_subfunction (dict): Requests grouped by SubFunction with details.
                Format: {
                    'SubFunction Name': {
                        'count': int,
                        'function_name': str,  # Parent Function name
                        'requests': [
                            {
                                'id': int,
                                'name': str,
                                'days_pending': int,  # Days in current stage
                                'stage': str,
                                'originator': str,
                                'current_stage_level': int
                            }
                        ],
                        'bpe_reviewers': [
                            {
                                'name': str,
                                'email': str,
                                'can_review': bool
                            }
                        ]
                    }
                }
            - oldest_days_pending (int): Days since oldest request entered its current stage.
    """
    pending_requests = find_pending_requests()

    if not pending_requests.exists():
        return {
            "total_pending": 0,
            "awaiting_bpe_count": 0,
            "awaiting_su_count": 0,
            "by_subfunction": {},
            "oldest_days_pending": 0,
        }

    # Initialize grouping dictionaries
    by_subfunction: Dict[str, Any] = {}
    total_non_draft = 0
    oldest_days_in_stage = 0
    awaiting_bpe_count = 0
    awaiting_su_count = 0

    for request in pending_requests:
        # Get current stage (latest transition)
        latest_transition = (
            Transition.objects.filter(request=request).order_by("-created").first()
        )

        if not latest_transition:
            continue

        current_stage = latest_transition.stage.level
        stage_name = latest_transition.stage.name

        # Skip DRAFT stage requests
        if current_stage == Stage.StageLevels.DRAFT:
            continue

        # Count non-draft requests
        total_non_draft += 1

        # Count requests by specific stages
        if current_stage == Stage.StageLevels.SUBMITTED:
            awaiting_bpe_count += 1
        elif current_stage == Stage.StageLevels.APPROVED_BY_BUSINESS_PROCESS_EXPERT:
            awaiting_su_count += 1

        # Calculate days pending IN CURRENT STAGE (not since request creation)
        days_in_current_stage = (timezone.now() - latest_transition.created).days

        # Track oldest days in current stage
        if days_in_current_stage > oldest_days_in_stage:
            oldest_days_in_stage = days_in_current_stage

        # Get all subfunctions for this resource
        resource_subfunctions = request.resource.subfunctions.select_related(
            "function"
        ).all()

        for subfunction in resource_subfunctions:
            if subfunction.name not in by_subfunction:
                # Initialize subfunction entry with Function name
                by_subfunction[subfunction.name] = {
                    "count": 0,
                    "function_name": subfunction.function.name,  # Store parent Function name
                    "requests": [],
                    "bpe_reviewers": [],
                }

            # Add request details
            by_subfunction[subfunction.name]["count"] += 1
            by_subfunction[subfunction.name]["requests"].append(
                {
                    "id": request.id,
                    "name": request.resource.name,
                    "days_pending": days_in_current_stage,  # Days in current stage
                    "stage": stage_name,
                    "originator": request.originator.user.email,
                    "current_stage_level": current_stage,
                }
            )

    # Find Business Process Expert reviewers for each SubFunction
    for subfunction_name, data in by_subfunction.items():
        subfunction_obj = SubFunction.objects.filter(name=subfunction_name).first()

        if subfunction_obj:
            # Find all Business Process Experts with access to this SubFunction
            bpe_accesses = (
                Access.objects.filter(
                    subfunctions=subfunction_obj,
                    access_revoked_date__isnull=True,
                    role__level=Role.RoleLevels.BUSINESS_PROCESS_EXPERT,
                )
                .select_related("user", "role")
                .distinct()
            )

            for access in bpe_accesses:
                # Check if they can review at SUBMITTED stage
                can_review_submitted = access.stage.filter(
                    level=Stage.StageLevels.SUBMITTED
                ).exists()

                data["bpe_reviewers"].append(
                    {
                        "name": f"{access.user.first_name} {access.user.last_name}",
                        "email": access.user.email,
                        "can_review": can_review_submitted,
                    }
                )

    return {
        "total_pending": total_non_draft,
        "awaiting_bpe_count": awaiting_bpe_count,
        "awaiting_su_count": awaiting_su_count,
        "by_subfunction": by_subfunction,
        "oldest_days_pending": oldest_days_in_stage,
    }


def get_request_status_change_details(request: Request) -> Optional[Dict[str, Any]]:
    """
    Gets details about a request status change for originator notification.

    This function retrieves information about the most recent status change
    to a request, including who made the change and any comments they provided.
    Used for notifying originators when their requests are approved, rejected, or require revisions.

    Accepts:
        * request (Request): The request that had a status change.

    Returns:
        * details (dict or None): Dictionary containing request details, or None if no transition found.
            Format: {
                'request_id': int,
                'resource_name': str,
                'originator_name': str,
                'originator_email': str,
                'current_stage': str,
                'current_stage_level': int,
                'stage_display': str,
                'reviewer_name': str,
                'reviewer_comments': str,
                'transition_date': datetime
            }
    """
    latest_transition = (
        Transition.objects.filter(request=request)
        .select_related("stage")
        .order_by("-created")
        .first()
    )

    if not latest_transition:
        LOGGER.warning(f"No transition found for request {request.id}")
        return None

    disposition = (
        Disposition.objects.filter(transition=latest_transition)
        .select_related("approver", "approver__user")
        .first()
    )

    reviewer_name = "System"
    reviewer_comments = ""

    if disposition and disposition.approver:
        reviewer_user = disposition.approver.user
        reviewer_name = f"{reviewer_user.first_name} {reviewer_user.last_name}"
        reviewer_comments = disposition.justification or ""

    return {
        "request_id": request.id,
        "resource_name": request.resource.name,
        "originator_name": f"{request.originator.user.first_name} {request.originator.user.last_name}",
        "originator_email": request.originator.user.email,
        "current_stage": latest_transition.stage.name,
        "current_stage_level": latest_transition.stage.level,
        "stage_display": get_stage_display(latest_transition.stage.level),
        "reviewer_name": reviewer_name,
        "reviewer_comments": reviewer_comments,
        "transition_date": latest_transition.created,
    }
