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
    "type": "test create type",
    "download": False,
    "originator": CREATE_REQUEST_USER_EMAIL,
    "stage": "PENDING",
}
