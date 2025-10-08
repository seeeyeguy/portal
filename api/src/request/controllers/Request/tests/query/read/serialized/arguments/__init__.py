"""
Arguments to be shared for RequestNotification's fetch
controller pytests.
"""

from typing import List

FETCH_REQUEST_NOTIFICATION_EXPECTED_NOTIFICATIONS: List[dict] = [
    {
        "request_id": 4,
        "subfunctions": [6],
        "originator": "May.Parker@harris.com",
        "stage": 4,
    },
    {
        "request_id": 5,
        "subfunctions": [5],
        "originator": "May.Parker@harris.com",
        "stage": 3,
    },
    {
        "request_id": 3,
        "subfunctions": [4],
        "originator": "May.Parker@harris.com",
        "stage": 2,
    },
]
