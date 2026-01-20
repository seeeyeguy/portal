"""
Arguments to be shared for Request's create
controller pytests.
"""

from django.core.files.base import File

from request.controllers.Request.Request import CreateRequestParams

# User email used when testing `Request` create.
CREATE_REQUEST_USER_EMAIL: str = "May.Parker@harris.com"

# User email used when testing `Request` create with a
# `User` that does not have `Access` with a valid `Role`.
CREATE_REQUEST_USER_EMAIL_INVALID_ROLE: str = "Gwen.Stacy@harris.com"

# Base parameters used for successful `Resource` creation.
BASE_CREATE_REQUEST_STRUCTURE_PARAMS: CreateRequestParams = {
    "uid": None,
    "previous_revision": None,
    "name": "Test Create Name",
    "description": "Test resource description for create tests.",
    "url": "https://www.test-site.com",
    "thumbnail": File(b""),  # type: ignore[typeddict-item,unused-ignore,arg-type]
    "employee_levels": [3],
    "subfunctions": [2, 5],
    "tags": [1, 2, 3],
    "point_of_contacts": ["May.Parker@l3harris.com"],
    "type": "test create type",
    "download": False,
    "originator": CREATE_REQUEST_USER_EMAIL,
    "stage": "DRAFT",
}

VALID_CREATED_REQUEST_DRAFT = {
    "resource": {
        "employee_levels": [
            {
                "id": 3,
                "name": "Executive",
                "description": "Executive Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 3,
            }
        ],
        "subfunctions": [
            {
                "id": 5,
                "function": {
                    "id": 3,
                    "name": "Finance",
                    "description": "Function 3.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Capital",
                "description": "Function 3 SubFunction 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 2,
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Recruiting",
                "description": "Function 1 SubFunction 2.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
        ],
        "tags": [
            {
                "id": 1,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Melbourne",
            },
            {
                "id": 2,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Rochester",
            },
            {
                "id": 3,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "restricted::department:GeoSpatial",
            },
        ],
        "primary_point_of_contact": "May.Parker@l3harris.com",
        "description": "Test resource description for create tests.",
        "revision_number": None,
        "name": "Test Create Name",
        "url": "https://www.test-site.com",
        "type": "test create type",
        "download": False,
        "active": False,
        "deleted": False,
        "previous_revision": None,
    },
    "originator": {
        "id": 3,
        "user": {
            "id": 1,
            "username": "May.Parker@harris.com",
            "email": "May.Parker@l3harris.com",
            "first_name": "May",
            "last_name": "Parker",
            "is_active": True,
        },
        "role": {
            "id": 3,
            "created": "2024-08-27T12:00:00-04:00",
            "name": "Data Steward",
            "description": "Data Steward.",
            "level": 3,
        },
        "stage": [],
        "subfunctions": [
            {
                "id": 5,
                "function": {
                    "id": 3,
                    "name": "Finance",
                    "description": "Function 3.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Capital",
                "description": "Function 3 SubFunction 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 6,
                "function": {
                    "id": 3,
                    "name": "Finance",
                    "description": "Function 3.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Cost Planning",
                "description": "Function 3 SubFunction 2.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 8,
                "function": {
                    "id": 4,
                    "name": "Operations",
                    "description": "Function 4.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "General",
                "description": "Function 4 SubFunction 2.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 4,
                "function": {
                    "id": 2,
                    "name": "Engineering",
                    "description": "Function 2.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Mechanical Engineering",
                "description": "Function 2 SubFunction 2.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 7,
                "function": {
                    "id": 4,
                    "name": "Operations",
                    "description": "Function 4.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Quality",
                "description": "Function 4 SubFunction 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 2,
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Recruiting",
                "description": "Function 1 SubFunction 2.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 3,
                "function": {
                    "id": 2,
                    "name": "Engineering",
                    "description": "Function 2.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Software Engineering",
                "description": "Function 2 SubFunction 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 1,
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Training",
                "description": "Function 1 SubFunction 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
        ],
        "access_granted_date": "2024-08-27T12:00:00-04:00",
        "access_revoked_date": None,
    },
    "status": "PENDING",
}

VALID_CREATED_REQUEST_SUBMITTED = {
    "resource": {
        "employee_levels": [
            {
                "id": 3,
                "name": "Executive",
                "description": "Executive Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 3,
            }
        ],
        "subfunctions": [
            {
                "id": 5,
                "function": {
                    "id": 3,
                    "name": "Finance",
                    "description": "Function 3.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Capital",
                "description": "Function 3 SubFunction 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 2,
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Recruiting",
                "description": "Function 1 SubFunction 2.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
        ],
        "tags": [
            {
                "id": 1,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Melbourne",
            },
            {
                "id": 2,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Rochester",
            },
            {
                "id": 3,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "restricted::department:GeoSpatial",
            },
        ],
        "primary_point_of_contact": "May.Parker@l3harris.com",
        "description": "Test resource description for create tests.",
        "revision_number": None,
        "name": "Test Create Name",
        "url": "https://www.test-site.com",
        "type": "test create type",
        "download": False,
        "active": False,
        "deleted": False,
        "previous_revision": None,
    },
    "originator": {
        "id": 3,
        "user": {
            "id": 1,
            "username": "May.Parker@harris.com",
            "email": "May.Parker@l3harris.com",
            "first_name": "May",
            "last_name": "Parker",
            "is_active": True,
        },
        "role": {
            "id": 3,
            "created": "2024-08-27T12:00:00-04:00",
            "name": "Data Steward",
            "description": "Data Steward.",
            "level": 3,
        },
        "stage": [],
        "subfunctions": [
            {
                "id": 5,
                "function": {
                    "id": 3,
                    "name": "Finance",
                    "description": "Function 3.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Capital",
                "description": "Function 3 SubFunction 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 6,
                "function": {
                    "id": 3,
                    "name": "Finance",
                    "description": "Function 3.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Cost Planning",
                "description": "Function 3 SubFunction 2.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 8,
                "function": {
                    "id": 4,
                    "name": "Operations",
                    "description": "Function 4.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "General",
                "description": "Function 4 SubFunction 2.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 4,
                "function": {
                    "id": 2,
                    "name": "Engineering",
                    "description": "Function 2.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Mechanical Engineering",
                "description": "Function 2 SubFunction 2.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 7,
                "function": {
                    "id": 4,
                    "name": "Operations",
                    "description": "Function 4.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Quality",
                "description": "Function 4 SubFunction 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 2,
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Recruiting",
                "description": "Function 1 SubFunction 2.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 3,
                "function": {
                    "id": 2,
                    "name": "Engineering",
                    "description": "Function 2.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Software Engineering",
                "description": "Function 2 SubFunction 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
            {
                "id": 1,
                "function": {
                    "id": 1,
                    "name": "Human Resources",
                    "description": "Function 1.",
                    "created": "2024-08-27T12:00:00-04:00",
                    "modified": "2024-08-27T12:00:00-04:00",
                },
                "name": "Training",
                "description": "Function 1 SubFunction 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
            },
        ],
        "access_granted_date": "2024-08-27T12:00:00-04:00",
        "access_revoked_date": None,
    },
    "status": "PENDING",
}
