"""
Signals to create and update `Profile`records for
each `User` created or updated in the application's
databases.
"""

# pylint: disable=imported-auth-user,unused-argument
from django.contrib.auth.models import User
from django.db import connections
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models.Profile.Profile import Profile

from manager.settings import ApplicationBuild, BUILD

PROFILE_TABLE: str = "users_profile"


@receiver(post_save, sender=User)
def create_user_profile(
    sender: User, instance: User, created: bool, **kwargs: dict
) -> None:
    """When a User is created, create an associated profile."""

    database_alias = kwargs["using"]

    if (
        BUILD != ApplicationBuild.TEST
        and created
        and database_alias in connections  # type: ignore[operator]
        # pylint: disable=line-too-long
        and PROFILE_TABLE in connections[database_alias].introspection.table_names()  # type: ignore[index]
    ):
        Profile.objects.using(database_alias).create(user=instance)  # type: ignore[arg-type]
        try:
            instance.profile.update_user_profile_ldap()
        except AttributeError:
            # Fail silently.
            pass


@receiver(post_save, sender=User)
def save_user_profile(sender: User, instance: User, **kwargs: dict) -> None:
    """When a User object is saved, save the associated profile."""

    try:
        database_alias = kwargs["using"]

        if (
            BUILD != ApplicationBuild.TEST
            and database_alias in connections  # type: ignore[operator]
            # pylint: disable=line-too-long
            and PROFILE_TABLE in connections[database_alias].introspection.table_names()  # type: ignore[index]
        ):
            instance.profile.update_user_profile_ldap()
    except AttributeError:
        # Fail silently.
        pass
