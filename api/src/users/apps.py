"""
App config module. UsersConfig provides
configuration settings to Django while it
sets up the `users` app.
"""

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
        from manager import settings

        User = get_user_model()

        def create_development_user(**_: dict) -> None:
            if settings.BUILD != settings.ApplicationBuild.DEVELOPMENT:
                return None

            LOGGER = logging.getLogger(__name__)

            LOGGER.info("Creating development user...")

            first_name = settings.SSO_DEVELOPMENT_USER["first_name"]
            last_name = settings.SSO_DEVELOPMENT_USER["last_name"]
            email = f"{first_name}.{last_name}@l3harris.com"
            password = settings.CONTAINER_PASSWORD

            if not User.objects.filter(email=email).exists():
                User.objects.create_superuser(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=password,
                )
            return None

        def load_initial_dataset(**_: dict) -> None:
            if settings.BUILD != settings.ApplicationBuild.DEVELOPMENT:
                return None

            call_command(
                "loaddata",
                "portal/db/init/data/init.json",
                verbosity=3,
                database="default",
            )

        post_migrate.connect(load_initial_dataset, sender=self, weak=False)
        post_migrate.connect(create_development_user, sender=self, weak=False)

        return super().ready()
