"""
Signals to create and update `User` records in
the `Program Review Tool` database for each `User`
created or updated in the `BI Portal` database.
"""

import logging

# pylint: disable=imported-auth-user,unused-argument
from django.contrib.auth.models import User
from django.db import connections, models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from manager.settings import ApplicationBuild, BUILD

LOGGER = logging.getLogger(__name__)

DATABASE_ALIAS: str = "prt"

USER_TABLE: str = "auth_user"


@receiver(post_save, sender=User)
def create_user_in_prt_database(
    sender: User, instance: User, created: bool, **_: dict
) -> None:
    """When a User is created in `BI Portal` database,
    create the same user in the `Program Review Tool`
    database.
    """

    LOGGER.info(f"Syncing user create: {instance.username}")

    if (
        BUILD != ApplicationBuild.TEST
        and created
        and DATABASE_ALIAS in connections
        and USER_TABLE in connections[DATABASE_ALIAS].introspection.table_names()
    ):
        user_queryset = User.objects.using(DATABASE_ALIAS).filter(
            username=instance.username
        )
        if not user_queryset.exists():
            User.objects.using(DATABASE_ALIAS).create(
                username=instance.username,
                email=instance.email,
                first_name=instance.first_name,
                last_name=instance.last_name,
                is_superuser=instance.is_superuser,
                password=instance.password,
                last_login=timezone.now(),
                is_staff=instance.is_staff,
                is_active=instance.is_active,
                date_joined=instance.date_joined,
            )


@receiver(post_save, sender=User)
def update_user_in_prt_database(sender: User, instance: User, **_: dict) -> None:
    """When a User object is saved in the `BI Portal` database,
    update the same user in the `Program Review Tool`
    database."""

    LOGGER.info(f"Syncing user update: {instance.username}")

    if (
        BUILD != ApplicationBuild.TEST
        and DATABASE_ALIAS in connections
        and USER_TABLE in connections[DATABASE_ALIAS].introspection.table_names()
    ):
        user_queryset = User.objects.using(DATABASE_ALIAS).filter(
            username=instance.username
        )
        if user_queryset.exists():
            user_queryset.update(
                email=instance.email,
                first_name=instance.first_name,
                last_name=instance.last_name,
                is_superuser=instance.is_superuser,
                last_login=instance.last_login,
                is_staff=instance.is_staff,
                is_active=instance.is_active,
            )
        else:
            User.objects.using(DATABASE_ALIAS).create(
                username=instance.username,
                email=instance.email,
                first_name=instance.first_name,
                last_name=instance.last_name,
                is_superuser=instance.is_superuser,
                password=instance.password,
                last_login=timezone.now(),
                is_staff=instance.is_staff,
                is_active=instance.is_active,
                date_joined=instance.date_joined,
            )
