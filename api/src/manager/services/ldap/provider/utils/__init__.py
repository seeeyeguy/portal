"""
Utility module that provides helper functions to facilitate
communication between interal API processes/functions/controllers
and the LDAP service.
"""

import json
import logging
from typing import List, Optional, Union

from django.contrib.auth import get_user_model, models
from django.db import DatabaseError, IntegrityError, transaction
from manager.services.ldap.provider import search_ldap

LOGGER = logging.getLogger(__name__)

User = get_user_model()


def fetch_employee_record_from_ldap(email: str) -> Union[dict, None]:
    """
    Fetch a L3Harris employee record from LDAP.

    Accepts:
        * email (str): An L3Harris employee email.

    Returns:
        * (dict | None): A record of employee data for the given
            email, including first name, last name, email, title,
            segment, and citizenship among others.
    """

    body = {"search_term": email, "offset": 1, "limit": 1}
    response = search_ldap(body)
    search_response = json.loads(response.content)
    entries: List[dict] = search_response["entries"]
    if len(entries) == 0:
        LOGGER.error(
            f"No user entries returned for provided email {email}.",
        )
        return None

    # Should never happen since emails should be unique, however LDAP service does not
    # assume that, therefore, checking to ensure only one entry is returned for the sake
    # of completeness.
    if len(entries) > 1:
        LOGGER.error(f"Expected to query to return 1 entry but got {len(entries)}.")
        return None

    return entries[0]


def fetch_authorized_employee(email: str) -> Optional[models.User]:
    """
    Fetch `User` instance if user of the application or
    an employee of L3Harris Technologies. inc

    Accepts:
        email: An L3Harris employee email.

    Returns:
        An instance of `User` if found, `None` otherwise.
    """

    user = User.objects.filter(email__iexact=email)
    if user.exists():
        return user.first()

    # Fetch user data from LDAP.
    user_info = fetch_employee_record_from_ldap(email=email)
    if not user_info:
        return None

    # If so, add user to system.
    LOGGER.info("Creating new user....")
    try:
        with transaction.atomic():
            new_user = User.objects.create(
                email=email.lower(),
                username=email.lower(),
                first_name=user_info["firstName"],
                last_name=user_info["lastName"],
            )
            LOGGER.info(f"New user created: {new_user}")
            return new_user
    except IntegrityError as exc:
        LOGGER.error(f"User ({email}) already exists: {exc}")
        return User.objects.filter(email__iexact=email).first()
    except DatabaseError:
        LOGGER.error(f"Could not create User ({email}).")
        return None
