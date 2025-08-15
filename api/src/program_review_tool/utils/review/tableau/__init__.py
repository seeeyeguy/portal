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
from typing import Optional, Tuple, Union
from xml.etree import ElementTree as ET

from django.core.cache import cache

from program_review_tool.exceptions import ProgramReviewToolError
from program_review_tool.utils.review.tableau.config import (
    TABLEAU_API_VERSION,
    TABLEAU_CA_CERTIFICATE,
    TABLEAU_PERSONAL_ACCESS_TOKENS,
    TABLEAU_SERVER,
)

from manager.settings import SERVER_HOST


LOGGER = logging.getLogger(__name__)

AUTH_URL: str = f"{TABLEAU_SERVER}/api/{TABLEAU_API_VERSION}/auth/signin"

VLE_HOSTNAME_PREFIX: str = "lnvle"

# Tableau auth token cache key prefix.
TABLEAU_AUTH_TOKEN_CACHE_KEY_PREFIX: str = (
    "program_review_tool_tableau_tableau_auth_token"
)

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
            timeout=180,
        )
        response.raise_for_status()
    except (requests.ConnectionError, requests.Timeout) as exc:
        LOGGER.error(f"Failed to retrieve image from '{url}': {exc}")
        raise ProgramReviewToolError(
            "Export generation service is unavailable. Please try again later.",
            529,
        ) from exc
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


def sign_in_to_tableau(token_name: str, token_secret: str) -> Optional[str]:
    """
    Authenticates with the Tableau Server using the provided
    PAT token name and secret and returns an authentication token.

    Accepts:
        * token_name (str): Name of the Tableau PAT token.
        * token_secret (str): Secret of the Tableau PAT token.

    Returns:
        * Optional[str]: The authentication token if successful; otherwise, None.
    """

    if not (token_name and token_secret):
        LOGGER.error("Tableau PAT name and secret must be set.")
        return None

    payload = f"""
    <tsRequest>
        <credentials personalAccessTokenName="{token_name}"
                     personalAccessTokenSecret="{token_secret}">
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


def get_tableau_token_for_job() -> Tuple[str, str]:
    """
    Returns an available Tableau token and its cache key.

    Accepts:
        * None

    Returns:
        * Tuple[str,str]: A tuple with an available Tableau
            token and its cache key if found and available
            for use.
    """

    # Query the cache using the Tableau token cache key prefix to
    # retrieve the collection of keys holding the Tableau tokens.
    token_cache_keys = cache.keys(f"*{TABLEAU_AUTH_TOKEN_CACHE_KEY_PREFIX}*")  # type: ignore[attr-defined]

    for token_cache_key in token_cache_keys:

        lock_key = f"{token_cache_key.upper()}-lock"
        lock_value = f"{token_cache_key}-locked"
        lock_timeout = 3
        # Attempt to set a lock (for 3 seconds) for the token key.
        if cache.set(lock_key, lock_value, lock_timeout, nx=True):  # type: ignore[call-arg,func-returns-value]
            token, in_use = cache.get(
                token_cache_key, (TABLEAU_AUTH_TOKEN_EXPIRATION_TEXT, False)
            )
            # If the token is not expired and is not in use and then
            # return it.
            if token != TABLEAU_AUTH_TOKEN_EXPIRATION_TEXT and not in_use:
                return token_cache_key, token
        else:
            # Token has been locked by another process, continue on the next
            # token cache key.
            continue
    return "", ""


def cache_tableau_auth_tokens() -> None:
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

    for token_name, token_secret in TABLEAU_PERSONAL_ACCESS_TOKENS.items():
        # Authenticate with Tableau to retrieve a valid token.
        token = sign_in_to_tableau(token_name, token_secret)
        # If sign in failed, log and continue.
        if token is None:
            err_msg = f"Tableau sign in failed for token: {token_name}"
            LOGGER.error(err_msg)
            continue

        tableau_auth_token_cache_key: str = (
            f"{TABLEAU_AUTH_TOKEN_CACHE_KEY_PREFIX}_{token_name}"
        )

        # Set the token in the cache with an initial in use flag value of False.
        cache.set(
            tableau_auth_token_cache_key, (token, False), TABLEAU_AUTH_CACHE_TIMEOUT
        )
