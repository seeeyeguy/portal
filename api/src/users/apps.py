"""
App config module. UsersConfig provides
configuration settings to Django while it
sets up the `users` app.
"""

from typing import cast

from django.apps import AppConfig
from django.db.models.signals import post_migrate

from django.utils import timezone


class UsersConfig(AppConfig):
    """App Config for Users app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self) -> None:
        """Perform initialization when app is ready."""

        # pylint: disable=import-outside-toplevel,invalid-name
        import logging
        import pandas as pd

        from django.contrib.auth import get_user_model
        from django.core.management import call_command

        from directory.models import Resource, Tag
        from request.models import Request
        from users.models import Access, Role

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
            username = f"{first_name}.{last_name}@harris.com"
            email = f"{first_name}.{last_name}@l3harris.com"
            password = settings.CONTAINER_PASSWORD

            if not User.objects.using(database_alias).filter(username__iexact=username).exists():
                dev_user = User.objects.using(database_alias).create(
                    username=username.lower(),
                    email=email.lower(),
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                    is_superuser=True,
                    is_staff=True,
                    is_active=True,
                )
                
                Access.objects.create(
                    user=dev_user,
                    role=Role.objects.get(level=1),
                    access_granted_date=timezone.now(),
                )

            return None

        def load_initial_dataset(**kwargs: dict) -> None:
            if settings.BUILD != settings.ApplicationBuild.DEVELOPMENT:
                return None

            if kwargs["using"] != DEFAULT_DATABASE_ALIAS:  # type: ignore[comparison-overlap]
                return None

            call_command(
                "loaddata",
                "portal/db/init/data/init-dev.json",
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

        def update_tag_labels(**kwargs: dict) -> None:
            """Update label of each tag to match its source within `master.xlsx`."""

            if settings.BUILD not in {
                settings.ApplicationBuild.DEVELOPMENT,
            }:
                return None

            if kwargs["using"] != DEFAULT_DATABASE_ALIAS:  # type: ignore[comparison-overlap]
                return None

            df = pd.read_excel(
                "portal/db/init/scripts/source/master.xlsx", sheet_name="CURATED"
            )

            LOGGER.info("Reading Tag Labels...")

            # Read normal tags from master source file.
            df_tags = df.dropna(subset=["Tags"])

            LOGGER.info("Updating Tag Labels...")

            # Create de-duped list of normal tags from master source file.
            tags = set()
            for tag in df_tags["Tags"]:
                labels = [label.strip() for label in tag.split(",")]
                labels = [label for label in labels if len(label)]
                tags |= set(labels)
            tags = list(tags)

            # Update tag labels to match those in the master source file.
            for tag in tags:
                Tag.objects.filter(label__iexact=tag).update(label=tag)

            LOGGER.info("Reading Site Labels...")

            # Read site tags from master source file.
            df_sites = df.dropna(subset=["Site"])

            LOGGER.info("Updating Site Labels...")

            # Create a de-duped list of site tags from the master source file.
            sites = set()
            for tag in df_sites["Site"]:
                sites.add(tag.strip())
            sites = list(sites)

            # Update site labels to match those in the master source file.
            for tag in sites:
                Tag.objects.filter(label__iexact=f"filter::site:{tag}").update(
                    label=f"filter::site:{tag}"
                )

        post_migrate.connect(load_initial_dataset, sender=self, weak=False)
        post_migrate.connect(create_development_user, sender=self, weak=False)
        post_migrate.connect(add_primary_point_of_contact, sender=self, weak=False)
        post_migrate.connect(update_tag_labels, sender=self, weak=False)

        return super().ready()
