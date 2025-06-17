"""
App config module. UsersConfig provides
configuration settings to Django while it
sets up the `users` app.
"""

from typing import cast

from django.apps import AppConfig
from django.db.models.signals import post_migrate


class UsersConfig(AppConfig):
    """App Config for Users app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self) -> None:
        """Perform initialization when app is ready."""

        # pylint: disable=import-outside-toplevel,invalid-name
        import logging

        from django.contrib.auth import get_user_model
        from django.core.management import call_command

        from directory.models import Resource
        from request.models import Request

        from manager import settings

        User = get_user_model()

        DEFAULT_DATABASE_ALIAS = "default"

        LOGGER = logging.getLogger(__name__)

        def create_development_user(**kwargs: dict) -> None:
            if settings.BUILD != settings.ApplicationBuild.DEVELOPMENT:
                return None

            LOGGER.info("Creating development user...")

            database_alias: str = cast(str, kwargs["using"])

            first_name = settings.SSO_DEVELOPMENT_USER["first_name"]
            last_name = settings.SSO_DEVELOPMENT_USER["last_name"]
            email = f"{first_name}.{last_name}@l3harris.com"
            password = settings.CONTAINER_PASSWORD

            if not User.objects.using(database_alias).filter(email=email).exists():
                User.objects.using(database_alias).create(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    is_superuser=True,
                    is_staff=True,
                    is_active=True,
                )
            return None

        def load_initial_dataset(**kwargs: dict) -> None:
            if settings.BUILD != settings.ApplicationBuild.DEVELOPMENT:
                return None

            if kwargs["using"] != DEFAULT_DATABASE_ALIAS:  # type: ignore[comparison-overlap]
                return None

            call_command(
                "loaddata",
                "portal/db/init/data/init.json",
                verbosity=3,
                database=DEFAULT_DATABASE_ALIAS,
            )

        def add_primary_point_of_contact(**kwargs: dict) -> None:
            """For all existing `Resource` records, create a related
            `PointOfContact` record that designates the originator
            of the `Resource`'s `Request` as the primary point of
            contact."""

            if settings.BUILD != settings.ApplicationBuild.DEVELOPMENT:
                return None

            if kwargs["using"] != DEFAULT_DATABASE_ALIAS:  # type: ignore[comparison-overlap]
                return None

            for record in Resource.objects.all():
                request = cast(Request, record.requests)
                originator = request.originator.user
                record.point_of_contacts.add(
                    originator, through_defaults={"primary": True}
                )

            row_count = Resource.objects.count()
            log_msg = f"Updated {row_count} Resource records..."
            LOGGER.info(log_msg)

        post_migrate.connect(load_initial_dataset, sender=self, weak=False)
        post_migrate.connect(create_development_user, sender=self, weak=False)
        post_migrate.connect(add_primary_point_of_contact, sender=self, weak=False)

        return super().ready()
