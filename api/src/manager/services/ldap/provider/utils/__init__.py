"""
Utility module that provides helper functions to facilitate
communication between interal API processes/functions/controllers
and the LDAP service.
"""

import json
import logging
import requests
from typing import List, Optional, Union

from django.contrib.auth import get_user_model, models
from django.db import DatabaseError, IntegrityError, transaction
from manager.services.ldap.provider import search_ldap

LOGGER = logging.getLogger(__name__)

User = get_user_model()


def fetch_employee_record_from_ldap(search_term: str) -> Union[dict, None]:
    """
    Fetch a L3Harris employee record from LDAP.

    Accepts:
        * search_term (str): L3Harris employee to search for.

    Returns:
        * (dict | None): A record of employee data for the given
            email, including first name, last name, email, title,
            segment, and citizenship among others.
    """

    body = {"search_term": search_term, "offset": 1, "limit": 1}
    try:
        response = search_ldap(body)
    except (requests.ConnectionError, requests.HTTPError) as exc:
        LOGGER.error(f"Unable to search LDAP: ${exc}")
        return None
    search_response = json.loads(response.content)
    entries: List[dict] = search_response["entries"]
    if len(entries) == 0:
        LOGGER.error(
            f"No user entries returned for provided search term: {search_term}.",
        )
        return None

    # Should never happen since emails should be unique, however LDAP service does not
    # assume that, therefore, checking to ensure only one entry is returned for the sake
    # of completeness.
    if len(entries) > 1:
        LOGGER.error(f"Expected to query to return 1 entry but got {len(entries)}.")
        return None

    return entries[0]


def fetch_employee_records_from_ldap(
    search_term: str,
    limit: int = 100,
) -> List[dict]:
    """
    Search LDAP and return matching entries.

    Accepts:
        * search_term (str): L3Harris employee to search for.
        * limit (int): Max records to return.

    Returns:
        List[dict]: a list of LDAP entry dicts; empty list if none found
    """
    body = {"search_term": search_term, "offset": 1, "limit": limit}
    try:
        response = search_ldap(body)
    except (requests.ConnectionError, requests.HTTPError) as exc:
        LOGGER.error(f"Unable to search LDAP: {exc}")
        return []

    search_response = json.loads(response.content)
    entries: List[dict] = search_response.get("entries", [])
    if not entries:
        LOGGER.warning(f"No LDAP entries returned for search term: {search_term}.")
    return entries


def fetch_authorized_employee(email: str, db: str = "default") -> Optional[models.User]:
    """
    Fetch `User` instance if user of the application or
    an employee of L3Harris Technologies. inc

    Accepts:
        email: An L3Harris employee email.
        db: Alias for database for which we will query for users.

    Returns:
        An instance of `User` if found, `None` otherwise.
    """

    if "@" not in email:
        return None

    # Search email first.
    user_q = User.objects.using(db).filter(email__iexact=email)
    if user_q.exists():
        return user_q.first()

    # Search username second.
    user_q = User.objects.using(db).filter(username__iexact=email)
    if user_q.exists():
        return user_q.first()

    # Fetch user data from LDAP.
    user_info = fetch_employee_record_from_ldap(search_term=email)
    if not user_info:
        return None

    # If user exists in LDAP, add user to system.
    LOGGER.info("Creating new user....")
    try:
        with transaction.atomic():
            new_user = User.objects.create(
                email=user_info["email"],
                username=user_info["username"],
                first_name=user_info["firstName"],
                last_name=user_info["lastName"],
            )
            LOGGER.info(f"New user created: {new_user}")
            return new_user
    except IntegrityError as exc:
        LOGGER.error(f"User ({email}) already exists: {exc}")
        user = User.objects.filter(email__iexact=user_info["email"]).first()
        if user:
            return user

        # If the email lookup fails, fall back to a username and update email.
        user_to_update = User.objects.get(username__iexact=user_info["username"])
        if user_to_update:
            _ = User.objects.filter(username__iexact=user_info["username"]).update(
                email=user_info["email"],
                first_name=user_info["firstName"],
                last_name=user_info["lastName"],
            )
            user_to_update.refresh_from_db()
            LOGGER.info(f"User updated: {user_to_update}")
            return user_to_update
        LOGGER.error(f"User not found, User ({user_info['username']}).")
        return None
    except DatabaseError:
        LOGGER.error(f"User not found, User ({user_info['username']}).")
        return None
