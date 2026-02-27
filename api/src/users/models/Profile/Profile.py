"""
`Profile` extends the `User` model with
insightful data queried from LDAP.
"""

from typing import cast
import logging
import urllib3
import requests

# pylint: disable=imported-auth-user,too-many-instance-attributes,no-member,unused-argument
from django.contrib.auth.models import User
from django.db import models, DatabaseError

from users.models.Segment.Segment import Segment

from manager.services.ldap.provider.utils import fetch_employee_records_from_ldap


LOGGER = logging.getLogger(__name__)


class Profile(models.Model):
    """Extra information about Users."""

    user: User = cast(User, models.OneToOneField(User, on_delete=models.CASCADE))

    # User id data.
    uid: models.CharField = models.CharField(max_length=64, blank=True, default="")

    # User name data.
    middle_initial: models.CharField = models.CharField(
        max_length=10, blank=True, default=""
    )

    # User UNIX login data.
    unix_name: models.CharField = models.CharField(
        max_length=15, blank=True, default=""
    )

    # Job data.
    job_title: models.CharField = models.CharField(
        max_length=256, blank=True, default=""
    )
    job_function: models.CharField = models.CharField(
        max_length=256, blank=True, default=""
    )
    job_family: models.CharField = models.CharField(
        max_length=256, blank=True, default=""
    )
    job_category: models.CharField = models.CharField(
        max_length=256, blank=True, default=""
    )
    job_level: models.IntegerField = models.IntegerField(null=True, default=None)

    # Employment metadata.
    account_type: models.CharField = models.CharField(
        max_length=256, blank=True, default=""
    )
    status: models.CharField = models.CharField(max_length=256, blank=True, default="")

    # Segment data.
    segment: models.ForeignKey = models.ForeignKey(
        Segment,
        db_column="segment",
        default=None,
        null=True,
        on_delete=models.SET_NULL,
    )
    division: models.CharField = models.CharField(
        max_length=256, blank=True, default=""
    )
    business_unit: models.CharField = models.CharField(
        max_length=256, blank=True, default=""
    )
    department: models.CharField = models.CharField(
        max_length=256, blank=True, default=""
    )

    # Location data.
    location: models.CharField = models.CharField(
        max_length=256, blank=True, default=""
    )
    citizenship: models.CharField = models.CharField(
        max_length=64, blank=True, default=""
    )

    def __str__(self) -> str:
        """String representation of a user profile."""

        # Create extra information about the user.
        # We know an email will always exist as its required.
        extra_information = f"email={self.user.email}"

        # We only want to add this information if all exists.
        if self.job_title and self.segment:
            extra_information = (
                f"{extra_information}, "
                f"job_title={self.job_title}, segment={self.segment}"
            )

        return (
            f"User[{self.user.last_name}, {self.user.first_name} ({extra_information})]"
        )

    def update_user_profile_ldap(self) -> None:
        """Update a user's profile with data fetched from LDAP."""

        try:
            full_name = f"{self.user.first_name} {self.user.last_name}".strip()
            ldap_entries = fetch_employee_records_from_ldap(full_name)
        except (
            requests.exceptions.ConnectionError,
            requests.HTTPError,
            urllib3.exceptions.MaxRetryError,
            urllib3.exceptions.NewConnectionError,
        ):
            return None

        if not ldap_entries:
            return None

        # Find the profile entry that belongs to this user.
        user_info = None
        for entry in ldap_entries:
            # `username` is the canonical SSO UPN (UserPrincipalName).
            ldap_username = entry.get("username")
            if ldap_username and ldap_username.lower() == self.user.username.lower():
                user_info = entry
                break

        if not user_info:
            LOGGER.warning(
                "No LDAP entry for user %s matched username %s",
                full_name,
                self.user.username,
            )
            return None

        LOGGER.info("Updating user profile...")

        self.uid = user_info.get("uid", "")
        self.middle_initial = user_info.get("middleInitial", "")
        self.unix_name = user_info.get("unixName", "")
        self.job_title = user_info.get("title", "")
        self.job_function = user_info.get("jobFunction", "")
        self.job_family = user_info.get("jobFamily", "")
        self.job_category = user_info.get("jobCategory", "")
        self.job_level = user_info.get("level", None)

        self.account_type = str(user_info.get("accountType", "")).upper()
        self.status = str(user_info.get("employmentStatus", "")).upper()
        try:
            model_db = self._state.db
            segment_instance = Segment.objects.using(model_db).filter(
                name__icontains=str(user_info["segment"])
            )
            if segment_instance.exists():
                self.segment = segment_instance.first()
        except DatabaseError:
            pass
        self.division = user_info.get("division", "")
        self.business_unit = user_info.get("businessUnit", "")
        self.department = user_info.get("department", "")

        self.location = user_info.get("location", "")
        self.citizenship = user_info.get("citizenship", "")

        ldap_email = user_info.get("email")
        if ldap_email and ldap_email != self.user.email:
            self.user.email = ldap_email
            # Persist only the email field to avoid an extra full‑save.
            self.user.save(update_fields=["email"])
            LOGGER.info("User email updated from LDAP: %s", ldap_email)

        self.save()
        return None
