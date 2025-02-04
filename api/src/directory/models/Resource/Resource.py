"""
`Resource` represents a link to an internal tool within L3Harris
technologies. These tools may be web applications, data services,
downloadable files, etc that provide employees a valuable resource
that they may use to help complete their tasking, or garner
important information. A `Resource` may be created by any user with
admin access, submitting a `Request` that moves through the request workflow
to its final approval. A `Resource` consists of several attributes, as well
as metadata that may be used to appropriately display a link. `Resource`s also
have an appropriately defined relationship to `SubFunction`, `EmployeeLevel`,
and `Tag`. Resource also has an indirect relationship to `Function` through
`SubFunction`. These relationships convey a method of categorizing, grouping,
and filtering resources.
"""

import logging
import os
import uuid

# pylint: disable=unused-argument
from django.db import models, DatabaseError
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from directory.exceptions import DirectoryError

from directory.models.Resource.types import ResourceModelType
from portal.models import BasicInformationAbstractModel, DateTimeAbstractModel

LOGGER = logging.getLogger(__name__)


def thumbnail_path(instance: ResourceModelType, filename: str) -> str:
    """
    Return the path to a thumbnail file for a `Resource`.

    Accepts:
        * instance (directory.models.Resource): An instance of `Resource`.
        * filename (str): Name of the file being stored.

    Returns:
        * (str): A path to the thumbnail file, where it will be saved.
    """

    # file will be uploaded to MEDIA_ROOT/.../<revision_id>/<id>/<filename>
    return f"resources/thumbnails/{instance.uid}/{instance.id}/{filename}"


class Resource(BasicInformationAbstractModel, DateTimeAbstractModel):
    """
    `Resource` represents a link to an internal tool within L3Harris
    Technologies. Resources act as a point of access for those internal
    tools, thus allowing `BI Portal` to function as a web directory.
    Resources serve as the primary content of the `BI Portal`.

    A `Resource` includes:
        * id (int): An auto-generated number managed by the database.
        * uid (models.UUIDField): A shared id for all revisions of the same resource.
        * previous_revision (directory.models.Resource): A reference to its previous
            revision.
        * revision_number (models.PositiveIntegerField): A number that
            uniquely identifies a resource amongst its revisions.
        * name (models.CharField): The name of the `Resource`.
        * description (models.CharField): A short/detailed description of what
            this `Resource` is.
        * url (models.URLField): The web address of a resource.
        * thumbnail (models.ImageField): An icon to display as a thumbnail for the
            resource.
        * employee_levels (models.ManyToManyField[directory.models.EmployeeLevel]):
            A set of `EmployeeLevel`s that relate to this `Resource`. EmployeeLevel
            helps to classify a resource, and provide metadata.
        * subfunctions (models.ManyToManyField[directory.models.SubFunction]): A set
            of `SubFunction`s that relate to this `Resource`. SubFunction helps to
            classify a resource, and provide metadata.
        * tags (models.ManyToManyField[directory.models.Tag]): A set of `Tag`s that
            relate to this `Resource`. Tag helps to classify a resource, and
            provide metadata.
        * type (models.CharField): A source for a `Resource`. Where the content may be
            stored.
        * download (models.BooleanField): Whether this `Resource` provides downloadable
            content.
        * active (model.BooleanField): Whether this `Resource` is available to the user.
        * created (models.DateTimeField): The date & time this `Resource` was created.
    """

    uid: models.UUIDField = models.UUIDField(default=uuid.uuid4)
    previous_revision: models.OneToOneField = models.OneToOneField(
        "self", null=True, on_delete=models.SET_NULL
    )
    revision_number: models.PositiveIntegerField = models.PositiveIntegerField()
    name: models.CharField = models.CharField(max_length=512)
    url: models.URLField = models.URLField(max_length=1024)
    thumbnail: models.ImageField = models.ImageField(
        upload_to=thumbnail_path, null=True
    )
    employee_levels: models.ManyToManyField = models.ManyToManyField(
        "directory.EmployeeLevel", db_table="directory_resource_employeelevels"
    )
    subfunctions: models.ManyToManyField = models.ManyToManyField(
        "directory.SubFunction", db_table="directory_resource_subfunctions"
    )
    tags: models.ManyToManyField = models.ManyToManyField(
        "directory.Tag", db_table="directory_resource_tags"
    )
    type: models.CharField = models.CharField(max_length=512)
    download: models.BooleanField = models.BooleanField(default=False)
    active: models.BooleanField = models.BooleanField(default=False)
    modified = None  # type: ignore[assignment]

    def __str__(self) -> str:
        """String Representation of `Resource`."""

        return f"Resource(id={self.id}, name={self.name}, url={self.url})"

    @property
    def id(self) -> int:
        """Primary Key."""

        return self.id

    class Meta:
        """Meta class for Resource."""

        db_table_comment = ""
        default_related_name = "resources"
        indexes = [
            models.Index(fields=("uid", "revision_number"), name="resource_revision"),
            models.Index(fields=("name",), name="resource_name"),
            models.Index(fields=("id",), name="resource_id"),
        ]
        ordering = ["name", "-created"]
        constraints = [
            models.UniqueConstraint(
                fields=["uid", "revision_number"], name="resource_revision_id"
            )
        ]
        verbose_name = "resource"
        verbose_name_plural = "resources"


Resource.Meta.db_table_comment = Resource.__doc__  # type: ignore[assignment]


@receiver(post_save, sender=Resource)
def update_uid_for_revision(
    sender: Resource, instance: Resource, **kwargs: dict
) -> None:
    """When a `Resource` object is saved, ensure that it
    shares the same uid as its previous revision."""

    try:
        if (
            instance.previous_revision
            and instance.uid != instance.previous_revision.uid
        ):
            LOGGER.info("Assigning `Resource` uid...")
            instance.uid = instance.previous_revision.uid
            instance.save()
    except (AttributeError, DatabaseError) as exc:
        error_message = "Assigning `Resource` uid failed."
        LOGGER.error(f"{error_message} {exc}")
        raise DirectoryError(error_message, 500) from exc


@receiver(pre_delete, sender=Resource)
def delete_resource_thumbnail(
    sender: Resource, instance: Resource, **kwargs: dict
) -> None:
    """When a `Resource` object is deleted, ensure to also
    delete its thumbnail from the server's filesystem."""

    try:
        if instance.thumbnail:
            LOGGER.info("Removing `Resource` thumbnail...")
            path_to_thumbnail = instance.thumbnail.path
            os.remove(path_to_thumbnail)
    except (AttributeError, DatabaseError, OSError) as exc:
        error_message = (
            "Unable to remove thumbnail for "
            f"Resource(id={instance.id}. name={instance.name})"
        )
        LOGGER.error(error_message)
        raise DirectoryError(error_message, 500) from exc
