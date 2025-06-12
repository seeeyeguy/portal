"""
Type annotations for `Resource` model.
`Resource` model depends on some functions,
but those functions need the `Resource` model
for typing so we need this module to prevent a
circular dependency in the model file.
"""

# pylint: disable=too-few-public-methods
from django.db import models


class ResourceModelType:
    """Type annotations for `Resource` model."""

    id: int
    uid: models.UUIDField
    previous_revision: models.ForeignKey
    revision_number: models.PositiveIntegerField
    name: models.CharField
    description: models.TextField
    url: models.URLField
    thumbnail: models.ImageField
    employee_levels: models.ManyToManyField
    subfunctions: models.ManyToManyField
    tags: models.ManyToManyField
    type: models.CharField
    download: models.BooleanField
    active: models.BooleanField
    deleted: models.BooleanField
