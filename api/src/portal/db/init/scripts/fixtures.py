""" 
Fixtures script module. Module provide utility classes that
may be used to create an initial fixtures dataset, that may
be loaded into the application's database using Django commands such
as `loaddata`. 
"""

import requests
from datetime import datetime
from typing import Any, cast, List, TypedDict, Union
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, validate_email
from rest_framework import status

from request.models.Request import Request as RequestModel

from manager.services.ldap.provider.utils import fetch_employee_record_from_ldap


class FixtureRecord(TypedDict):
    """Type annotation for a record fixture."""

    model: str
    pk: int
    fields: dict[str, Any]


class FixtureDataAddedIndexRecordMappings(TypedDict):
    """Type annotation for class fixtures with an extra
    index for record mappings."""

    records: List[FixtureRecord]
    mappings: dict[str, dict[str, FixtureRecord]]


class FixtureDataRecordMappings(TypedDict):
    """Type annotation for class fixture data with record mappings."""

    records: List[FixtureRecord]
    mappings: dict[str, Union[dict[str, Any], FixtureRecord]]


class FixtureDataTransitionRecordMappings(FixtureDataAddedIndexRecordMappings):
    """Type annotation for `Transition` class fixture data with an extra index
    for record mappings."""

    previous_transitions: dict[str, Union[str, None]]


class FixtureDataPKMappings(TypedDict):
    """Type annotation for class fixture data with pk mappings."""

    records: List[FixtureRecord]
    mappings: dict[str, int]


class Users:
    """
    Container class for functionality related to creating
    and managing fixtures for the `Users` app.
    """

    class Role:
        """
        `Role` represents an access role in the application. A `Role`
        conveys permissions to a `User`. Within `BI Portal`, we
        have a limited set of roles, including `Superuser`,
        `Business Process Expert`, & `Data Steward`.
        """

        class AdminRoles:
            """Valid admin roles for BI Portal."""

            SUPERUSER = "Superuser"
            BUSINESS_PROCESS_EXPERT = "Business Process Expert"
            DATA_STEWARD = "Data Steward"

        roles: FixtureDataPKMappings = {
            "records": [
                {
                    "model": "users.role",
                    "pk": 1,
                    "fields": {
                        "name": AdminRoles.SUPERUSER,
                        "description": "Superuser.",
                        "level": 1,
                        "created": datetime.now().isoformat(),
                    },
                },
                {
                    "model": "users.role",
                    "pk": 2,
                    "fields": {
                        "name": AdminRoles.BUSINESS_PROCESS_EXPERT,
                        "description": "Business Process Expert.",
                        "level": 2,
                        "created": datetime.now().isoformat(),
                    },
                },
                {
                    "model": "users.role",
                    "pk": 3,
                    "fields": {
                        "name": AdminRoles.DATA_STEWARD,
                        "description": "Data Steward.",
                        "level": 3,
                        "created": datetime.now().isoformat(),
                    },
                },
            ],
            "mappings": {
                AdminRoles.SUPERUSER: 1,
                AdminRoles.BUSINESS_PROCESS_EXPERT: 2,
                AdminRoles.DATA_STEWARD: 3,
            },
        }

        next_id = 4

    class User:
        """
        `User` represents a user within the application. Users have access to
        application and may engage with its functionality.
        """

        # Stakeholders that have admin access.
        admins = ["nathaniel.charbonneau@harris.com", "melissa.cataldo@harris.com"]

        # Developers that have admin access.
        staff = [
            "michael.c.mullings@harris.com",
            "sabrina.dion@harris.com",
            "luis.ruelaslisboa@harris.com",
            "jesse.rehrer@harris.com",
        ]

        # Fixture data and mappings.
        users: FixtureDataRecordMappings = {
            "records": [],
            "mappings": {},
        }

        next_id = 1

        @staticmethod
        def _create_record(
            user_id: int,
            email: str,
            first_name: str,
            last_name: str,
            is_staff: bool = False,
            is_superuser: bool = False,
        ) -> FixtureRecord:
            """Create a `User` fixture."""

            return {
                "model": "auth.user",
                "pk": user_id,
                "fields": {
                    "username": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "is_staff": is_staff,
                    "is_superuser": is_superuser,
                    "is_active": True,
                    "date_joined": datetime.now().isoformat(),
                },
            }

        @staticmethod
        def add_record(email: str, first_name: str, last_name: str) -> None:
            """Add a user record to `User` fixture dataset."""

            invalid_err = f"Email({email}) is not valid."
            duplicate_err = f"User with email({email}) already exists."

            is_staff = email.lower() in Users.User.staff
            is_superuser = email.lower() in [*Users.User.staff, *Users.User.admins]

            try:
                validate_email(email)
            except ValidationError as exc:
                raise ValueError(invalid_err) from exc

            employee_record = fetch_employee_record_from_ldap(email=email)

            if employee_record is None:
                raise ValueError(invalid_err)

            if email in Users.User.users["mappings"]:
                raise ValueError(duplicate_err)

            record = Users.User._create_record(
                Users.User.next_id, email, first_name, last_name, is_staff, is_superuser
            )

            Users.User.users["records"].append(record)
            Users.User.users["mappings"][email] = record
            Users.User.next_id += 1

    class Access:
        """
        `Access` represents an individual access within the
        application associated with a role.
        """

        accesses: FixtureDataAddedIndexRecordMappings = {
            "records": [],
            "mappings": {},
        }

        next_id = 1

        @staticmethod
        def _create_record(
            access_id: int, user: str, role: int, stages: List[int]
        ) -> FixtureRecord:
            """Create a `Access` record."""

            return {
                "model": "users.access",
                "pk": access_id,
                "fields": {
                    "user": user,
                    "role": role,
                    "access_granted_date": datetime.now().isoformat(),
                    "access_revoked_date": None,
                    "stage": stages,
                },
            }

        @staticmethod
        def add_access_record(user: str, role: str, stages: List[str]) -> None:
            """Add an access record to `Access` fixture dataset."""

            invalid_user_err = f"User({user}) is not a valid user."
            invalid_role_err = f"Role({user}) is not a valid role."
            invalid_stages_err = f"Stages({stages}) are not valid."
            duplicate_err = f"Access for User({user}) with Role({role}) already exists."

            stage_ids = []

            if user not in Users.User.users["mappings"]:
                raise ValueError(invalid_user_err)

            if role not in Users.Role.roles["mappings"]:
                raise ValueError(invalid_role_err)

            for stage in stages:
                if stage not in Request.Stage.stages["mappings"]:
                    raise ValueError(invalid_stages_err)
                stage_ids.append(Request.Stage.stages["mappings"][stage])

            if (
                user in Users.Access.accesses["mappings"]
                and role in Users.Access.accesses["mappings"][user]
            ):
                raise ValueError(duplicate_err)

            record = Users.Access._create_record(
                Users.Access.next_id,
                user,
                Users.Role.roles["mappings"][role],
                stage_ids,
            )

            Users.Access.accesses["records"].append(record)
            if user in Users.Access.accesses["mappings"]:
                Users.Access.accesses["mappings"][user][role] = record
            else:
                Users.Access.accesses["mappings"][user] = {
                    role: record,
                }
            Users.Access.next_id += 1


class Request:
    """
    Container class for functionality related to creating
    and managing fixtures for the `Request` app.
    """

    class Stage:
        """
        `Stage` represents a single phase in the resource request
        workflow.
        """

        class WorkflowStages:
            """Valid stages of BI Portal workflow."""

            DRAFT = "Draft"
            SUBMITTED = "Submitted"
            APPROVED_BY_BUSINESS_PROCESS_EXPERT = "Approved by Business Process Expert"
            REVISE = "Revise"
            REJECTED_BY_BUSINESS_PROCESS_EXPERT = "Rejected by Business Process Expert"
            APPROVED_BY_SUPERUSER = "Approved by Superuser"
            REJECTED_BY_SUPERUSER = "Rejected by Superuser"

        stages: FixtureDataPKMappings = {
            "records": [
                {
                    "model": "request.stage",
                    "pk": 1,
                    "fields": {
                        "name": WorkflowStages.DRAFT,
                        "description": "A resource was created.",
                        "level": 1,
                    },
                },
                {
                    "model": "request.stage",
                    "pk": 2,
                    "fields": {
                        "name": WorkflowStages.SUBMITTED,
                        "description": "A resource was submitted.",
                        "level": 2,
                    },
                },
                {
                    "model": "request.stage",
                    "pk": 3,
                    "fields": {
                        "name": WorkflowStages.APPROVED_BY_BUSINESS_PROCESS_EXPERT,
                        "description": "A resource was approved by the Business Process Expert.",
                        "level": 3,
                    },
                },
                {
                    "model": "request.stage",
                    "pk": 4,
                    "fields": {
                        "name": WorkflowStages.REVISE,
                        "description": "An edit to the draft was requested.",
                        "level": 4,
                    },
                },
                {
                    "model": "request.stage",
                    "pk": 5,
                    "fields": {
                        "name": WorkflowStages.REJECTED_BY_BUSINESS_PROCESS_EXPERT,
                        "description": "A resource was rejected by the Business Process Expert.",
                        "level": 5,
                    },
                },
                {
                    "model": "request.stage",
                    "pk": 6,
                    "fields": {
                        "name": WorkflowStages.APPROVED_BY_SUPERUSER,
                        "description": "A resource was approved by a Superuser.",
                        "level": 99,
                    },
                },
                {
                    "model": "request.stage",
                    "pk": 7,
                    "fields": {
                        "name": WorkflowStages.REJECTED_BY_SUPERUSER,
                        "description": "A resource was rejected by a Superuser.",
                        "level": 100,
                    },
                },
            ],
            "mappings": {
                WorkflowStages.DRAFT: 1,
                WorkflowStages.SUBMITTED: 2,
                WorkflowStages.APPROVED_BY_BUSINESS_PROCESS_EXPERT: 3,
                WorkflowStages.REVISE: 4,
                WorkflowStages.REJECTED_BY_BUSINESS_PROCESS_EXPERT: 5,
                WorkflowStages.APPROVED_BY_SUPERUSER: 6,
                WorkflowStages.REJECTED_BY_SUPERUSER: 7,
            },
        }

        next_id = 8

    class Request:
        """
        `Request` represents a request made by a user, to add, or modify
        a directory resource.
        """

        requests: FixtureDataRecordMappings = {
            "records": [],
            "mappings": {},
        }

        next_id = 1

        @staticmethod
        def _create_record(
            request_id: int, resource: int, originator: int
        ) -> FixtureRecord:
            """Create a `Request` record."""

            return {
                "model": "request.request",
                "pk": request_id,
                "fields": {
                    "resource": resource,
                    "originator": originator,
                    "status": RequestModel.RequestStatus.APPROVED,
                    "created": datetime.now().isoformat(),
                    "modified": datetime.now().isoformat(),
                },
            }

        @staticmethod
        def add_request_record(resource: str, originator: str) -> None:
            """Add a request record to `Request` fixture dataset."""

            invalid_access_err = f"Access({originator}) is not valid."
            duplicate_err = f"Request for Resource({resource}) already exists."

            if resource not in Directory.Resource.resources["mappings"]:
                raise ValueError(f"Resource({resource}) is not valid.")

            if not (
                originator in Users.Access.accesses["mappings"]
                and (
                    Users.Role.AdminRoles.DATA_STEWARD
                    in Users.Access.accesses["mappings"][originator]
                    or Users.Role.AdminRoles.SUPERUSER
                    in Users.Access.accesses["mappings"][originator]
                )
            ):
                raise ValueError(invalid_access_err)

            if resource in Request.Request.requests["mappings"]:
                raise ValueError(duplicate_err)

            access = (
                Users.Access.accesses["mappings"][originator][
                    Users.Role.AdminRoles.DATA_STEWARD
                ]
                if Users.Role.AdminRoles.DATA_STEWARD
                in Users.Access.accesses["mappings"][originator]
                else Users.Access.accesses["mappings"][originator][
                    Users.Role.AdminRoles.SUPERUSER
                ]
            )

            record = Request.Request._create_record(
                Request.Request.next_id,
                Directory.Resource.resources["mappings"][resource]["pk"],
                access["pk"],
            )

            Request.Request.requests["records"].append(record)
            Request.Request.requests["mappings"][resource] = record
            Request.Request.next_id += 1

    class Transition:
        """
        `Transition` represents the transition of a `Resource`
        from one `Stage` to another.
        """

        transitions: FixtureDataTransitionRecordMappings = {
            "records": [],
            "mappings": {},
            "previous_transitions": {
                "Draft": None,
                "Submitted": "Draft",
                "Approved by Superuser": "Submitted",
            },
        }

        next_id = 1

        @staticmethod
        def _create_record(
            transition_id: int,
            request: int,
            stage: int,
            previous_transition: Union[int, None],
        ) -> FixtureRecord:
            """Create a `Transition` record."""

            return {
                "model": "request.transition",
                "pk": transition_id,
                "fields": {
                    "request": request,
                    "stage": stage,
                    "previous_transition": previous_transition,
                    "created": datetime.now().isoformat(),
                },
            }

        @staticmethod
        def add_transition_record(resource: str, stage: str) -> None:
            """Add a transition record to `Transition` fixture dataset."""

            invalid_resource_err = f"Resource({resource}) is not valid."
            invalid_stage_err = f"Stage({stage}) is not valid."
            duplicate_err = f"Resource({resource}) at Stage({stage}) already exists."

            if resource not in Request.Request.requests["mappings"]:
                raise ValueError(invalid_resource_err)

            if (
                stage not in Request.Stage.stages["mappings"]
                or stage not in Request.Transition.transitions["previous_transitions"]
            ):
                raise ValueError(invalid_stage_err)

            previous_stage = Request.Transition.transitions["previous_transitions"][
                stage
            ]
            if previous_stage is not None:
                previous_transition = Request.Transition.transitions["mappings"][
                    resource
                ][previous_stage]["pk"]
            else:
                previous_transition = None

            if (
                resource in Request.Transition.transitions["mappings"]
                and stage in Request.Transition.transitions["mappings"][resource]
            ):
                raise ValueError(duplicate_err)

            record = Request.Transition._create_record(
                Request.Transition.next_id,
                Request.Request.requests["mappings"][resource]["pk"],
                Request.Stage.stages["mappings"][stage],
                previous_transition,
            )

            Request.Transition.transitions["records"].append(record)
            if resource in Request.Transition.transitions["mappings"]:
                Request.Transition.transitions["mappings"][resource][stage] = record
            else:
                Request.Transition.transitions["mappings"][resource] = {stage: record}
            Request.Transition.next_id += 1

    class Disposition:
        """
        `Disposition` represents a vote by a BI Portal admin
        on a request to add/modify a directory resource.
        """

        dispositions: FixtureDataAddedIndexRecordMappings = {
            "records": [],
            "mappings": {},
        }

        next_id = 1

        @staticmethod
        def _create_record(
            disposition_id: int, approver: int, transition: int
        ) -> FixtureRecord:
            """Create a `Disposition` record."""

            return {
                "model": "request.disposition",
                "pk": disposition_id,
                "fields": {
                    "approver": approver,
                    "disposition": "APPROVED",
                    "justification": "",
                    "transition": transition,
                    "created": datetime.now().isoformat(),
                },
            }

        @staticmethod
        def add_disposition_record(resource: str, stage: str, approver: str) -> None:
            """Add a disposition record to `Disposition` fixture dataset."""

            invalid_resource_err = f"Resource({resource}) is not valid."
            invalid_stage_err = f"Stage({stage}) is not valid."
            invalid_approver_err = f"Approver({approver}) is not valid."
            duplicate_err = (
                f"Disposition for Transition(Resource({resource})",
                f" and Stage({stage})) already exists.",
            )

            if resource not in Request.Transition.transitions["mappings"]:
                raise ValueError(invalid_resource_err)

            if (
                stage != Request.Stage.WorkflowStages.SUBMITTED
                or stage not in Request.Transition.transitions["mappings"][resource]
            ):
                raise ValueError(invalid_stage_err)

            if not (
                approver in Users.Access.accesses["mappings"]
                and Users.Role.AdminRoles.SUPERUSER
                in Users.Access.accesses["mappings"][approver]
            ):
                raise ValueError(invalid_approver_err)

            if (
                resource in Request.Disposition.dispositions["mappings"]
                and stage in Request.Disposition.dispositions["mappings"][resource]
            ):
                raise ValueError(duplicate_err)

            record = Request.Disposition._create_record(
                Request.Disposition.next_id,
                Users.Access.accesses["mappings"][approver][
                    Users.Role.AdminRoles.SUPERUSER
                ]["pk"],
                Request.Transition.transitions["mappings"][resource][stage]["pk"],
            )

            Request.Disposition.dispositions["records"].append(record)
            Request.Disposition.dispositions["mappings"][resource] = {stage: record}
            Request.Disposition.next_id += 1


class Directory:
    """
    Container class for functionality related to creating
    and managing fixtures for the `Directory` app.
    """

    class EmployeeLevel:
        """
        `EmployeeLevel` represents a hierarchical level of leadership within
        the organization and a level of concern for a resource.
        """

        class EmployeeLevelValues:
            """Valid employee levels for `BI Portal` resources."""

            EMPLOYEE = "Employee"
            MANAGER = "Manager"
            EXECUTIVE = "Executive"

        employee_levels: FixtureDataPKMappings = {
            "records": [
                {
                    "model": "directory.employeelevel",
                    "pk": 1,
                    "fields": {
                        "name": EmployeeLevelValues.EMPLOYEE,
                        "description": "Employee Level 1.",
                        "level": 1,
                        "created": datetime.now().isoformat(),
                        "modified": datetime.now().isoformat(),
                    },
                },
                {
                    "model": "directory.employeelevel",
                    "pk": 2,
                    "fields": {
                        "name": EmployeeLevelValues.MANAGER,
                        "description": "Manager Level 1.",
                        "level": 2,
                        "created": datetime.now().isoformat(),
                        "modified": datetime.now().isoformat(),
                    },
                },
                {
                    "model": "directory.employeelevel",
                    "pk": 3,
                    "fields": {
                        "name": EmployeeLevelValues.EXECUTIVE,
                        "description": "Executive Level 1.",
                        "level": 3,
                        "created": datetime.now().isoformat(),
                        "modified": datetime.now().isoformat(),
                    },
                },
            ],
            "mappings": {
                EmployeeLevelValues.EMPLOYEE: 1,
                EmployeeLevelValues.MANAGER: 2,
                EmployeeLevelValues.EXECUTIVE: 3,
            },
        }

    class Function:
        """
        `Function` represents a primary organizational unit that encompasses
        a broad area of expertise and responsibilities within the organization.
        """

        functions: FixtureDataRecordMappings = {
            "records": [],
            "mappings": {},
        }

        next_id = 1

        @staticmethod
        def _create_record(
            function_id: int, name: str, description: str
        ) -> FixtureRecord:
            """Create a `Function` record."""

            return {
                "model": "directory.function",
                "pk": function_id,
                "fields": {
                    "name": name,
                    "description": description,
                    "created": datetime.now().isoformat(),
                    "modified": datetime.now().isoformat(),
                },
            }

        @staticmethod
        def add_function_record(name: str, description: str) -> None:
            """Add a function record to `Function` fixture dataset."""

            duplicate_err = f"Function({name}) already exists."

            if name in Directory.Function.functions["mappings"]:
                raise ValueError(duplicate_err)

            record = Directory.Function._create_record(
                Directory.Function.next_id,
                name.encode("ascii", "ignore").decode(),
                description.encode("ascii", "ignore").decode(),
            )

            Directory.Function.functions["records"].append(record)
            Directory.Function.functions["mappings"][name] = record
            Directory.Function.next_id += 1

    class SubFunction:
        """
        `SubFunction` represents a specialized division within a `Function`
        that focuses on a more specific area of expertise.
        """

        subfunctions: FixtureDataRecordMappings = {
            "records": [],
            "mappings": {},
        }

        next_id = 1

        @staticmethod
        def _create_record(
            subfunction_id: int, name: str, description: str, function: int
        ) -> FixtureRecord:
            """Create a `SubFunction` record."""

            return {
                "model": "directory.subfunction",
                "pk": subfunction_id,
                "fields": {
                    "name": name,
                    "description": description,
                    "function": function,
                    "created": datetime.now().isoformat(),
                    "modified": datetime.now().isoformat(),
                },
            }

        @staticmethod
        def add_subfunction_record(name: str, description: str, function: str) -> None:
            """Add a subfunction record to `SubFunction` fixture dataset."""

            invalid_function_err = f"Function({function}) is not valid."
            duplicate_err = f"SubFunction({name}) already exists."

            if function not in Directory.Function.functions["mappings"]:
                raise ValueError(invalid_function_err)

            if name in Directory.SubFunction.subfunctions["mappings"]:
                raise ValueError(duplicate_err)

            record = Directory.SubFunction._create_record(
                Directory.SubFunction.next_id,
                name.encode("ascii", "ignore").decode(),
                description.encode("ascii", "ignore").decode(),
                Directory.Function.functions["mappings"][function]["pk"],
            )

            Directory.SubFunction.subfunctions["records"].append(record)
            Directory.SubFunction.subfunctions["mappings"][name] = record
            Directory.SubFunction.next_id += 1

    class Tag:
        """
        `Tag` represents a keyword, used to classify a resource.
        Tags consist primary of an arbitrary label, created by
        a superuser.
        """

        tags: FixtureDataRecordMappings = {
            "records": [],
            "mappings": {},
        }

        next_id = 1

        @staticmethod
        def _create_record(tag_id: int, label: str) -> FixtureRecord:
            """Create a `Tag` record."""

            return {
                "model": "directory.tag",
                "pk": tag_id,
                "fields": {
                    "label": label,
                    "created": datetime.now().isoformat(),
                    "modified": datetime.now().isoformat(),
                },
            }

        @staticmethod
        def _create_reserved_tag_record(
            tag_id: int, category: str, key: str, value: str
        ) -> FixtureRecord:
            """Create a reserved `Tag` record."""

            return Directory.Tag._create_record(tag_id, f"{category}::{key}:{value}")

        @staticmethod
        def _create_filter_tag_record(
            tag_id: int, key: str, value: str
        ) -> FixtureRecord:
            """Create a filter `Tag` record."""

            return Directory.Tag._create_reserved_tag_record(
                tag_id, "filter", key, value
            )

        @staticmethod
        def _create_restricted_tag_record(
            tag_id: int, key: str, value: str
        ) -> FixtureRecord:
            """Create a restricted `Tag` record."""

            return Directory.Tag._create_reserved_tag_record(
                tag_id, "restricted", key, value
            )

        @staticmethod
        def add_tag_record(
            label: str, tag_type: Union[str, None] = None, key: Union[str, None] = None
        ) -> None:
            """Add a tag record to `Tag` fixture dataset."""

            if tag_type == "restricted":
                record = Directory.Tag._create_restricted_tag_record(
                    Directory.Tag.next_id,
                    cast(str, key),
                    label.encode("ascii", "ignore").decode(),
                )
            elif tag_type == "filter":
                record = Directory.Tag._create_filter_tag_record(
                    Directory.Tag.next_id,
                    cast(str, key),
                    label.encode("ascii", "ignore").decode(),
                )
            else:
                record = Directory.Tag._create_record(
                    Directory.Tag.next_id, label.encode("ascii", "ignore").decode()
                )

            if record["fields"]["label"] in Directory.Tag.tags["mappings"]:
                raise ValueError(f"Tag({record['fields']['label']}) already exists.")

            Directory.Tag.tags["records"].append(record)
            Directory.Tag.tags["mappings"][record["fields"]["label"]] = record
            Directory.Tag.next_id += 1

    class Resource:
        """
        `Resource` represents a link to an internal tool within L3Harris
        Technologies.
        """

        resources: FixtureDataRecordMappings = {
            "records": [],
            "mappings": {},
        }

        next_id = 1

        @staticmethod
        def _create_record(
            resource_id: int,
            name: str,
            description: str,
            url: str,
            employee_levels: List[int],
            subfunctions: List[int],
            tags: List[int],
            resource_type: str,
            download: bool = False,
        ) -> FixtureRecord:
            """Create a `Resource` record."""

            return {
                "model": "directory.Resource",
                "pk": resource_id,
                "fields": {
                    "uid": str(uuid4()),
                    "previous_revision": None,
                    "revision_number": 1,
                    "name": name,
                    "description": description,
                    "url": url,
                    "thumbnail": "",
                    "employee_levels": employee_levels,
                    "subfunctions": subfunctions,
                    "tags": tags,
                    "type": resource_type,
                    "download": download,
                    "active": True,
                    "created": datetime.now().isoformat(),
                },
            }

        @staticmethod
        def add_resource_record(
            name: str,
            description: str,
            url: str,
            employee_levels: List[str],
            subfunctions: List[str],
            tags: List[str],
            resource_type: str,
            download: bool = False,
        ) -> None:
            """Add a tag record to `Tag` fixture dataset."""

            invalid_url_err = f"URL({url}) is not valid."
            invalid_employee_levels_err = (
                f"Employee Levels({employee_levels}) are not valid."
            )
            invalid_subfunctions_err = f"SubFunctions({subfunctions}) are not valid."
            invalid_tags_err = f"Tags({tags}) are not valid."
            duplicate_err = f"Resource({name}) already exists."

            employee_level_ids = []
            subfunctions_ids = []
            tag_ids = []

            if name in Directory.Resource.resources["mappings"]:
                raise ValueError(duplicate_err)

            validate = URLValidator()
            try:
                validate(url)
                res = requests.get(url=url, verify=False)
                if res.status_code == status.HTTP_404_NOT_FOUND:
                    raise ValidationError("404 - Not Found")
            except (ValidationError, requests.HTTPError) as exc:
                raise ValueError(invalid_url_err) from exc

            for employee_level in employee_levels:
                if (
                    employee_level
                    not in Directory.EmployeeLevel.employee_levels["mappings"]
                ):
                    raise ValueError(invalid_employee_levels_err)
                employee_level_ids.append(
                    Directory.EmployeeLevel.employee_levels["mappings"][employee_level]
                )

            for subfunction in subfunctions:
                if subfunction not in Directory.SubFunction.subfunctions["mappings"]:
                    raise ValueError(invalid_subfunctions_err)
                subfunctions_ids.append(
                    Directory.SubFunction.subfunctions["mappings"][subfunction]["pk"]
                )

            for tag in tags:
                if tag not in Directory.Tag.tags["mappings"]:
                    raise ValueError(invalid_tags_err)
                tag_ids.append(Directory.Tag.tags["mappings"][tag]["pk"])

            record = Directory.Resource._create_record(
                Directory.Resource.next_id,
                name.encode("ascii", "ignore").decode(),
                description.encode("ascii", "ignore").decode(),
                url,
                employee_level_ids,
                subfunctions_ids,
                tag_ids,
                resource_type,
                download,
            )

            Directory.Resource.resources["records"].append(record)
            Directory.Resource.resources["mappings"][name] = record
            Directory.Resource.next_id += 1
