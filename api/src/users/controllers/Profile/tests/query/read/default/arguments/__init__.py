"""
Arguments to be shared for Profile's fetch
controller pytests.
"""

# Valid `User` email.
VALID_PROFILE_USER_EMAIL: str = "May.Parker@harris.com"

# Valid `User` email but wrong user.
WRONG_VALID_PROFILE_USER_EMAIL: str = "Peter.Parker@harris.com"

# Invalid `User` email.
INVALID_PROFILE_USER_EMAIL: str = "DNE@harris.com"

# Valid `Profile` record dictionary.
VALID_PROFILE_DICTIONARY = {
    "id": 1,
    "user": {
        "id": 1,
        "username": "May.Parker@harris.com",
        "email": "May.Parker@l3harris.com",
        "first_name": "May",
        "last_name": "Parker",
        "is_active": True,
    },
    "segment": {
        "id": 1,
        "name": "SPACE & AIRBORNE SYSTEMS",
        "description": "Space & Airborne Systems is a provider of mission solutions.",
    },
    "uid": "618549",
    "middle_initial": "M",
    "unix_name": "U194879",
    "job_title": "Sr Assoc, Software Engrg",
    "job_function": "Engineering",
    "job_family": "Software Engineering",
    "job_category": "Person",
    "job_level": 2,
    "account_type": "Employee",
    "status": "Active",
    "division": "ESI",
    "business_unit": "GCS",
    "department": "SW-Image Processing",
    "location": "FL",
    "citizenship": "US",
}
