"""
Segment model module. Segment provides data
validation for profile data, aligning with the
different business segments of L3Harris Technologies.
Model serves to ensure that only a valid segment is
listed under a user's profile.segment.
"""

import inspect
from typing import Iterable

from django.db import models
from rest_framework import serializers

# SEGMENT REFERENCES
SAS = (1, "SAS", "SPACE & AIRBORNE SYSTEMS")
IMS = (2, "IMS", "INTEGRATED MISSION SYSTEMS")
CS = (3, "CS", "COMMUNICATION SYSTEMS")
AR = (4, "AR", "AEROJET ROCKETDYNE")

SEGMENT_ALIAS = {
    SAS[1]: SAS[2],
    IMS[1]: IMS[2],
    CS[1]: CS[2],
    AR[1]: AR[2],
}


class Segment(models.Model):
    """
    Represents a single segment of business
    at L3Harris Technologies, inc.

    A segment includes:
        1. id - an auto-generated number managed by the db.
        2. name - the name of the segment as denoted by L3Harris Technologies.
        3. description - a description of the segment's
        business function and intent.
    """

    class SegmentChoices:
        """Valid Choices for a business segment within L3Harris Technologies."""

        SPACE_AND_AIRBORNE_SYSTEMS = "SPACE & AIRBORNE SYSTEMS"
        INTEGRATED_MISSION_SYSTEMS = "INTEGRATED MISSION SYSTEMS"
        COMMUNICATION_SYSTEMS = "COMMUNICATION SYSTEMS"
        AEROJET_ROCKETDYNE = "AEROJET ROCKETDYNE"

        @classmethod
        def get_segment_choices(cls) -> Iterable[tuple[str, str]]:
            """Construct proper choices for Segment.name field."""

            segment_choices: list[tuple[str, str]] = []
            private_members_and_functions = ("_", "get")

            # getmembers() returns all the
            # members of an object.
            for member in inspect.getmembers(cls):
                # Remove private and protected
                # functions.
                if not member[0].lower().startswith(private_members_and_functions):
                    value = member[1]
                    label = member[0]
                    segment_choices.append((value, label))
            return segment_choices

    # Name of segment (should be full/complete).
    name: models.CharField = models.CharField(
        max_length=512,
        choices=SegmentChoices.get_segment_choices,  # type: ignore[arg-type]
    )
    # Describes the overall mission of the business segment.
    description: models.TextField = models.TextField()

    def __str__(self) -> str:
        return str(self.name)


class SegmentSerializer(serializers.ModelSerializer):
    """Serializer for segments."""

    class Meta:
        """Meta class for serializer."""

        model = Segment
        fields = "__all__"
