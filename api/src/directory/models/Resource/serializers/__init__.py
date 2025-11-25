"""
Serializers for `Resource` model. Serializers convert
python objects to JSON.
"""

from typing import Union

from rest_framework import serializers

from directory.models.Resource.PointOfContact import PointOfContact
from directory.models.Resource.Resource import Resource

from directory.models.EmployeeLevel.serializers import EmployeeLevelSerializer
from directory.models.SubFunction.serializers import SubFunctionSerializer
from directory.models.Tag.serializers import TagSerializer


class ResourceSerializer(serializers.ModelSerializer):
    """Model Base Serializer for `Resource`."""

    def to_representation(self, instance: Resource) -> dict:
        record: dict = super().to_representation(instance)
        # Primary POC
        primary_point_of_contact: Union[
            PointOfContact, None
        ] = PointOfContact.objects.filter(resource=instance, primary=True).first()
        poc_email = None
        if primary_point_of_contact:
            poc_email = primary_point_of_contact.contact.email

        record["primary_point_of_contact"] = poc_email

        # Secondary POCs
        secondary_point_of_contacts: list[PointOfContact] = list(
            PointOfContact.objects.filter(resource=instance, primary=False)
        )
        secondary_emails: list[str] = [
            poc.contact.email for poc in secondary_point_of_contacts
        ]
        if secondary_emails:  # only include if non-empty
            record["secondary_point_of_contacts"] = secondary_emails

        return record

    employee_levels = EmployeeLevelSerializer(many=True, read_only=True)
    subfunctions = SubFunctionSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        """Meta for `Resource` serializer."""

        model = Resource
        exclude = ["point_of_contacts"]
