"""
BI Portal `Directory` utils module. Common functionality for the
BI Portal `Directory` app.
"""

import requests

from django.core.validators import URLValidator
from rest_framework import status

from manager.settings import ApplicationBuild, BUILD, SERVER_HOST

# Request timeout (in seconds) for URL validation.
REQUEST_TIMEOUT: int = 5

VLE_HOSTNAME_PREFIX: str = "lnvle"


def validate_url(url: str) -> None:
    """Validate that the URL is both well-formed and reachable."""

    validate = URLValidator()
    validate(url)
    if (
        not SERVER_HOST.lower().startswith(VLE_HOSTNAME_PREFIX)
        and BUILD != ApplicationBuild.TEST
    ):
        res = requests.get(url=url, verify=False, timeout=REQUEST_TIMEOUT)
        if res.status_code == status.HTTP_404_NOT_FOUND:
            raise requests.HTTPError("404 - Not Found")
