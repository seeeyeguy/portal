"""
Type module for model. This module provides
custom types for a generic model instance.
Sometimes, a model's exact type may be ambiguous
but we want to describe attributes common to
some subset of model instances so we must create our
own types and place them here.
"""

from typing import TypedDict


class DjangoModelMetaType(TypedDict):
    """Type annotation for Django model metadata."""

    app_label: str


class DjangoModelType(TypedDict):
    """Type annotation for Django model."""

    _meta: DjangoModelMetaType
