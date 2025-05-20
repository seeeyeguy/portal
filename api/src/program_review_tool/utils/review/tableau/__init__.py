"""
`Program Review Tool` `Program` review Tableau utils module. Common
functionality for the `Program Review Tool` `Program` app to help
with retrieving `Program` data from the L3Harris Tableau
server.
"""

# pylint: disable=wrong-import-order
import logging
import os
import requests
from typing import Optional, Union
from xml.etree import ElementTree as ET

from django.core.cache import cache

from program_review_tool.utils.review.tableau.config import (
    TABLEAU_API_VERSION,
    TABLEAU_CA_CERTIFICATE,
    TABLEAU_PERSONAL_ACCESS_TOKEN_NAME,
    TABLEAU_PERSONAL_ACCESS_TOKEN_SECRET,
    TABLEAU_SERVER,
)

from manager.settings import SERVER_HOST


LOGGER = logging.getLogger(__name__)

AUTH_URL: str = f"{TABLEAU_SERVER}/api/{TABLEAU_API_VERSION}/auth/signin"

VLE_HOSTNAME_PREFIX: str = "lnvle"

# Tableau auth token cache key.
TABLEAU_AUTH_TOKEN_CACHE_KEY: str = "program_review_tool_tableau_tableau_auth_token"

# Tableau token cache expiration string.
TABLEAU_AUTH_TOKEN_EXPIRATION_TEXT: str = "has_expired"

# Cache timeout for token (72 hours in seconds).
TABLEAU_AUTH_CACHE_TIMEOUT: int = 259200


def _get_request_verify_option() -> Union[str, bool]:
    """
    Returns the path of the certificate to be used in
    a request call if it exists else will return boolean
    value True.

    Accepts:
        * None

    Returns:
        * verify_option (Union[str,bool]): The path of the
            certificate if it exists, else True.

    """

    verify_option: Union[str, bool] = (
        TABLEAU_CA_CERTIFICATE if os.path.exists(TABLEAU_CA_CERTIFICATE) else True
    )
    if isinstance(verify_option, bool):
        warning_msg: str = (
            f"Tableau CA certificate: '{TABLEAU_CA_CERTIFICATE}' not found."
            f" Using system certificates."
        )
        LOGGER.error(warning_msg)
    return verify_option


def get_and_save_view_image(url: str, file_path_name: str, token: str) -> bool:
    """
    Downloads an image from Tableau and saves it to the specified file path.

    Accepts:
        * url (str): URL to download the image from.
        * file_path_name (str): Path where the image will be saved.
        * token (str): Tableau authentication token.

    Returns:
        * bool: True if the image is saved successfully, False otherwise.
    """

    if not token:
        LOGGER.error("No Tableau authentication token provided.")
        return False

    verify_option = _get_request_verify_option()

    try:
        response = requests.get(
            url,
            headers={"Content-type": "application/xml", "X-Tableau-Auth": token},
            verify=verify_option,
            timeout=60,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        LOGGER.error(f"Failed to retrieve image from '{url}': {exc}")
        return False

    try:
        with open(file_path_name, "wb") as f:
            f.write(response.content)
        LOGGER.info(f"Image successfully saved to '{file_path_name}'.")
        return True
    except IOError as exc:
        LOGGER.error(f"Error saving image to '{file_path_name}': {exc}")
        return False


def sign_in_to_tableau() -> Optional[str]:
    """
    Authenticates with the Tableau Server and returns an authentication token.

    Accepts:
        * None

    Returns:
        * Optional[str]: The authentication token if successful; otherwise, None.
    """

    if not (
        TABLEAU_PERSONAL_ACCESS_TOKEN_NAME and TABLEAU_PERSONAL_ACCESS_TOKEN_SECRET
    ):
        LOGGER.error("Tableau PAT name and secret must be set.")
        return None

    payload = f"""
    <tsRequest>
        <credentials personalAccessTokenName="{TABLEAU_PERSONAL_ACCESS_TOKEN_NAME}"
                     personalAccessTokenSecret="{TABLEAU_PERSONAL_ACCESS_TOKEN_SECRET}">
            <site contentUrl="" />
        </credentials>
    </tsRequest>
    """

    verify_option = _get_request_verify_option()

    try:
        response = requests.post(
            AUTH_URL,
            data=payload,
            headers={"Content-type": "application/xml"},
            verify=verify_option,
            timeout=60,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        err_msg = f"Failed to sign in to Tableau server '{TABLEAU_SERVER}': {exc}"
        LOGGER.error(err_msg)
        return None

    try:
        root = ET.fromstring(response.content)
        namespace = {"t": "http://tableau.com/api"}
        token_element = root.find(".//t:credentials", namespace)
        if token_element is not None:
            token = token_element.attrib.get("token")
            LOGGER.info("Successfully authenticated with Tableau.")
            return token
        else:
            LOGGER.error("Authentication token not found in the response.")
            return None
    except ET.ParseError as exc:
        LOGGER.error(f"XML parsing error during authentication: {exc}")
        return None
    except Exception as exc:
        LOGGER.error(f"Unexpected error during Tableau sign in: {exc}")
        return None


def cache_tableau_auth_token() -> None:
    """
    Signs-in to L3Harris Tableau server
    and stores the retrieved authentication
    token in the cache.

    Accepts:
        * None

    Returns:
        * None
    """

    if SERVER_HOST.lower().startswith(VLE_HOSTNAME_PREFIX):
        info_msg = "Can't sign to Tableau due to no connection to L3Harris network."
        LOGGER.info(info_msg)
        return None

    # Authenticate with Tableau to retrieve a valid token.
    token = sign_in_to_tableau()
    # If sign in failed, log and return.
    if token is None:
        err_msg = "Tableau sign in failed. Exiting."
        LOGGER.error(err_msg)
        return None

    # Set the token in the cache.
    cache.set(TABLEAU_AUTH_TOKEN_CACHE_KEY, token, TABLEAU_AUTH_CACHE_TIMEOUT)

    LOGGER.info("Successfully stored Tableau token in cache.")
