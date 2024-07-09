"""
Provider module that proxies requests to
the LDAP service. 
"""

import logging
import requests

from django import http

from manager.settings import LDAP_SEARCH_ENDPOINT
from manager.services.exceptions import LDAPServiceError

LOGGER = logging.getLogger(__name__)


def search_ldap(body: dict) -> http.JsonResponse:
    """
    Query LDAP Search service.

    Accepts:
        body: A POST request body.
    Raises:
        LDAPServiceError: If LDAP_SEARCH_ENDPOINT setting is undefined.
    Returns:
        An LDAP Search service response containing the matching employee entries.
    """

    assert LDAP_SEARCH_ENDPOINT is not None, LDAPServiceError(
        "LDAP search endpoint is not defined.", status=500
    )

    LOGGER.info("Querying LDAP Search service...")
    res = requests.post(LDAP_SEARCH_ENDPOINT, json=body, timeout=480)
    res.raise_for_status()
    data = res.json()
    return http.JsonResponse(data)
