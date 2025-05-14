"""
Arguments to be shared for Disposition's create
controller pytests.
"""

# Arguments for successfully creating `Disposition` record.
CREATE_DISPOSITION_USER: str = "Tony.Stark@harris.com"
CREATE_DISPOSITION_REQUEST_ID: int = 1

# Valid `Disposition` values.
CREATE_DISPOSITION_APPROVED_DISPOSITION: str = "APPROVED"
CREATE_DISPOSITION_REJECTED_DISPOSITION: str = "REJECTED"
CREATE_DISPOSITION_REVISE_DISPOSITION: str = "REVISE"

# Invalid `Disposition` value.
CREATE_DISPOSITION_INVALID_DISPOSITION: str = "INVALID"

# Valid `Disposition` justifications.
CREATE_DISPOSITION_REJECTED_JUSTIFICATION: str = "Test Reject."
CREATE_DISPOSITION_REVISE_JUSTIFICATION: str = "Test Revise."

# Invalid `User` email for testing failure case.
CREATE_DISPOSITION_USER_DNE: str = "DNE.User@harris.com"

# `User` email that corresponds to a revoked `Access` for testing failure case.
CREATE_DISPOSITION_REVOKED_USER_ACCESS: str = "Miles.Morales@harris.com"

# `User` email for testing when a `User` does not have access to vote
# on the current `Stage`.
CREATE_DISPOSITION_USER_INVALID_ACCESS_FOR_STAGE: str = "May.Parker@harris.com"

# Invalid `Request` id for testing failure case.
CREATE_DISPOSITION_REQUEST_DNE: int = 9999

# `Request` id for testing create `Disposition` where the latest `Transition`
# is not at a valid voting `Stage`.
CREATE_DISPOSITION_INVALID_STAGE_REQUEST_ID: int = 2

# `Request` id for testing create `Disposition` on an active `Resource` record.
CREATE_DISPOSITION_ACTIVE_RESOURCE_REQUEST_ID: int = 3

# `Request` id for testing create `Disposition` on a historical `Resource` record.
CREATE_DISPOSITION_HISTORICAL_RESOURCE_REQUEST_ID: int = 4

# `Resource` id for testing create `Disposition` where a `Transition` does not exist.
CREATE_DISPOSITION_TRANSITION_DNE_REQUEST_ID: int = 6

# Expected values for created `APPROVED` `Disposition`.
CREATE_DISPOSITION_APPROVED_EXPECTED_VALUES: dict = {
    "approver": {
        "id": 1,
        "user": {
            "id": 3,
            "username": "Tony.Stark@harris.com",
            "email": "Tony.Stark@harris.com",
            "first_name": "Tony",
            "last_name": "Stark",
            "is_active": True,
        },
        "role": {"id": 1, "name": "Superuser", "description": "Superuser.", "level": 1},
        "stage": [
            {
                "id": 2,
                "name": "Submitted",
                "description": "A resource was submitted.",
                "level": 2,
            },
            {
                "id": 3,
                "name": "Approved by Business Process Expert",
                "description": "A resource was approved by the Business Process Expert.",
                "level": 3,
            },
        ],
    },
    "transition": 3,
    "disposition": "APPROVED",
    "justification": "",
}

# Expected values for created `REJECTED` `Disposition`.
CREATE_DISPOSITION_REJECTED_EXPECTED_VALUES: dict = {
    "approver": {
        "id": 1,
        "user": {
            "id": 3,
            "username": "Tony.Stark@harris.com",
            "email": "Tony.Stark@harris.com",
            "first_name": "Tony",
            "last_name": "Stark",
            "is_active": True,
        },
        "role": {"id": 1, "name": "Superuser", "description": "Superuser.", "level": 1},
        "stage": [
            {
                "id": 2,
                "name": "Submitted",
                "description": "A resource was submitted.",
                "level": 2,
            },
            {
                "id": 3,
                "name": "Approved by Business Process Expert",
                "description": "A resource was approved by the Business Process Expert.",
                "level": 3,
            },
        ],
    },
    "transition": 3,
    "disposition": "REJECTED",
    "justification": "Test Reject.",
}

# Expected values for created `REVISE` `Disposition`.
CREATE_DISPOSITION_REVISE_EXPECTED_VALUES: dict = {
    "approver": {
        "id": 1,
        "user": {
            "id": 3,
            "username": "Tony.Stark@harris.com",
            "email": "Tony.Stark@harris.com",
            "first_name": "Tony",
            "last_name": "Stark",
            "is_active": True,
        },
        "role": {"id": 1, "name": "Superuser", "description": "Superuser.", "level": 1},
        "stage": [
            {
                "id": 2,
                "name": "Submitted",
                "description": "A resource was submitted.",
                "level": 2,
            },
            {
                "id": 3,
                "name": "Approved by Business Process Expert",
                "description": "A resource was approved by the Business Process Expert.",
                "level": 3,
            },
        ],
    },
    "transition": 3,
    "disposition": "REVISE",
    "justification": "Test Revise.",
}
