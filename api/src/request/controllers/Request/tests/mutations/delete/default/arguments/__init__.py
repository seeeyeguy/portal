"""
Arguments to be shared for Request's delete
controller pytests.
"""

from django.core.files.base import File

from request.controllers.Request.Request import DeleteRequestParams

# User email used when testing `Request` delete.
DELETE_REQUEST_USER_EMAIL: str = "May.Parker@harris.com"

# Resource ID used when testing `Request` delete for a `Resource`
DELETE_REQUEST_RESOURCE_ID: int = 1

# User email used when testing `Request` delete with a
# `User` that does not have an `Access` with a valid `Role`.
DELETE_REQUEST_USER_EMAIL_INVALID_ROLE: str = "Gwen.Stacy@harris.com"

# Resource ID used when testing `Request` delete for a `Resource`
# that already has an open `Request`.
DELETE_REQUEST_RESOURCE_ID_HAS_REQUEST_OPEN: int = 2


# Base parameters used for successful `Resource` deletion.
BASE_DELETE_REQUEST_STRUCTURE_PARAMS: DeleteRequestParams = {
    "resource_id": DELETE_REQUEST_RESOURCE_ID,
    "originator": DELETE_REQUEST_USER_EMAIL,  # type: ignore
}

VALID_DELETE_REQUEST = {
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
        "primary_point_of_contact": "May.Parker@harris.com",
        "description": "Test resource description for delete tests.",
        "revision_number": None,
        "name": "Test Delete Name",
        "url": "https://www.test-site.com",
        "type": "test delete type",
        "download": False,
        "active": False,
        "deleted": True,
        "previous_revision": DELETE_REQUEST_RESOURCE_ID,
    },
    "originator": {
        "id": 3,
        "user": {
            "id": 1,
            "username": "May.Parker@harris.com",
            "email": "May.Parker@harris.com",
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
