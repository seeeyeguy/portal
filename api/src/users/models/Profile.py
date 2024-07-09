""" 
Profile model module. Profile extends the User
model with insightful data queried from LDAP. 
"""

from typing import cast
import logging
import urllib3
import requests

# pylint: disable=imported-auth-user,too-many-instance-attributes,no-member,unused-argument
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from manager.services.ldap.provider.utils import fetch_employee_record_from_ldap
from users.models.Segment import Segment

LOGGER = logging.getLogger(__name__)


class Profile(models.Model):
    """Extra information about Users."""

    user: User = cast(User, models.OneToOneField(User, on_delete=models.CASCADE))

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
            user_info = fetch_employee_record_from_ldap(self.user.email)
        except (
            requests.exceptions.ConnectionError,
            requests.HTTPError,
            urllib3.exceptions.MaxRetryError,
            urllib3.exceptions.NewConnectionError,
        ):
            return None

        if not user_info:
            return None

        LOGGER.info("Updating user profile...")

        self.job_title = user_info.get("title", "")
        self.job_function = user_info.get("jobFunction", "")
        self.job_family = user_info.get("jobFamily", "")
        self.job_category = user_info.get("jobCategory", "")
        self.job_level = user_info.get("level", None)

        self.account_type = str(user_info.get("accountType", "")).upper()
        self.status = str(user_info.get("employmentStatus", "")).upper()

        segment_instance = Segment.objects.filter(
            name__icontains=str(user_info["segment"])
        )
        if segment_instance.exists():
            self.segment = segment_instance.first()
        self.division = user_info.get("division", "")
        self.business_unit = user_info.get("businessUnit", "")
        self.department = user_info.get("department", "")

        self.location = user_info.get("location", "")
        self.citizenship = user_info.get("citizenship", "")

        self.save()
        return None


@receiver(post_save, sender=User)
def create_user_profile(
    sender: User, instance: User, created: bool, **kwargs: dict
) -> None:
    """When a User is created, create an associated profile."""

    if created:
        Profile.objects.create(user=instance)
        try:
            instance.profile.update_user_profile_ldap()
        except AttributeError:
            # Fail silently.
            pass


@receiver(post_save, sender=User)
def save_user_profile(sender: User, instance: User, **kwargs: dict) -> None:
    """When a User object is saved, save the associated profile."""

    try:
        instance.profile.update_user_profile_ldap()
    except AttributeError:
        # Fail silently.
        pass
