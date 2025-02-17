"""
Arguments to be shared for Visit's create
controller pytests.
"""

# pylint: disable=line-too-long

# `User` email used for testing create `Visit`.
CREATE_VISIT_USER_EMAIL: str = "May.Parker@harris.com"

# `Resource` id used for testing create `Visit`.
CREATE_VISIT_RESOURCE_ID: int = 1

# `User` DNE email used for testing failure case.
CREATE_VISIT_USER_EMAIL_DNE: str = "DNE.USER@harris.com"

# `Resource` DNE id used for testing failure case.
CREATE_VISIT_RESOURCE_ID_DNE: int = 9999

# Valid `Visit` to validate creation.
VALID_CREATED_VISIT: dict = {
    "resource": {
        "id": 1,
        "employee_levels": [
            {
                "id": 1,
                "name": "Employee",
                "description": "Employee Level 1.",
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "level": 1,
            }
        ],
        "subfunctions": [
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
            }
        ],
        "tags": [
            {
                "id": 1,
                "created": "2024-08-27T12:00:00-04:00",
                "modified": "2024-08-27T12:00:00-04:00",
                "label": "filter::site:Melbourne",
            }
        ],
        "description": "Resource 1 Revision 1 description.",
        "created": "2024-10-01T12:00:00-04:00",
        "uid": "fa1d4316-3d9a-44be-950e-7cb0b88f49f8",
        "revision_number": 1,
        "name": "Resource 1 Revision 1",
        "url": "example-site.org",
        "thumbnail": "/v1/media/resources/thumbnails/fa1d4316-3d9a-44be-950e-7cb0b88f49f8/1/resource_1.png",
        "primary_point_of_contact": "May.Parker@harris.com",
        "type": "Resource Type 1",
        "download": False,
        "active": True,
        "previous_revision": None,
    },
    "user": "May.Parker@harris.com",
}
