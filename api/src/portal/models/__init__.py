"""
BI Portal Base models used for inheritance. 
"""

from typing import cast

from django.contrib.auth import models as DjangoAuthModels, get_user_model
from django.db import models

# Application user model.
User: DjangoAuthModels.User = cast(DjangoAuthModels.User, get_user_model())


class BasicInformationAbstractModel(models.Model):
    """
    Represents an abstract model for basic information,
    common to several models. This model is never to be
    instantiated but merely, used for inheritance to keep
    code DRY.

    BasicInformationAbstractModel specification is to adhere to the
    following:
        - name (models.CharField): The name of the object.
        - description (models.TextField): A short/detailed description of what
            the object is.
    """

    name: models.CharField = models.CharField(max_length=512, unique=True)
    description: models.TextField = models.TextField()

    class Meta:
        """Model Meta Specification."""

        abstract = True


class DateTimeAbstractModel(models.Model):
    """
    Represents an abstract model for datetime metadata.
    This model is never to be instantiated but merely,
    used for inheritance to keep code DRY.

    DateTimeAbstractModel specification is to adhere to the
    following:

    - created (models.DateTimeField): The date & time the object was created.
    - modified (models.DateTimeField): The date & time the object was last
        modified.
    """

    created: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, editable=False
    )
    modified: models.DateTimeField = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        """Model Meta Specification."""

        abstract = True
