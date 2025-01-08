"""
Django admin command to append data to the database from a JSON fixture.
"""

import json
import logging
from typing import Any

from django.apps import apps
from django.core.management.base import BaseCommand, CommandParser

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    """Django admin command to append data to the database from a JSON fixture."""

    help = "Append data to the database from a JSON fixture."

    def add_arguments(self, parser: CommandParser) -> None:
        """Add argument for the path to the JSON fixture."""

        parser.add_argument("file_path", type=str, help="Path to the JSON fixture.")

    def handle(self, *args: Any, **options: str) -> None:
        """
        Read the JSON file and create new records in the database if they
        don't already exist.
        """

        objects = []

        with open(options["file_path"], encoding="utf-8") as json_file:
            objects = json.load(json_file)

        for obj in objects:
            model = apps.get_model(obj["model"])
            model_name = model._meta.object_name
            object_query = model.objects.filter(**obj["fields"])

            if not object_query.exists():
                new_record = model.objects.create(**obj["fields"])
                LOGGER.info(f"Created {model_name} record with id: {new_record.id}.")
            else:
                LOGGER.info(
                    f"{model_name} record with attributes: {obj['fields']} "
                    "already exists!"
                )
