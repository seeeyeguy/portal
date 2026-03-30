"""
Authenticate with PowerBI and return a token.
Includes token pooling for concurrent job support.

FIXED: 
- Added extract_token_string() to handle nested tuples
- Added is_token_expired() to check JWT expiration
- All token retrieval now extracts clean strings
- All token storage uses consistent format
"""

# pylint: disable=wrong-import-order
import base64
import json
import logging
import os
import time
import requests, ssl
from typing import Optional, Tuple, Union, Any
from xml.etree import ElementTree as ET

from django.core.cache import cache

from program_review_tool.exceptions import ProgramReviewToolError
from program_review_tool.utils.review.powerbi.config import ( 
    AZURE_TENANT_ID,
    AZURE_CLIENT_ID,
    AZURE_CLIENT_SECRET,
    AZURE_TOKEN_CACHE_KEY,
    AZURE_TOKEN_CACHE_KEY_EXPIRES_IN,
    AZURE_TOKEN_CACHE_KEY_EXPIRES_ON
)

LOGGER = logging.getLogger(__name__)

# Azure token cache expiration string.
AZURE_AUTH_TOKEN_EXPIRATION_TEXT: str = "has_expired"

# Cache timeout for token (1hr, minus 10%).
AZURE_AUTH_CACHE_TIMEOUT: int = int(os.getenv("AZURE_AUTH_CACHE_TIMEOUT", 3240))

# Number of tokens to maintain in the pool for concurrent jobs
TOKEN_POOL_SIZE: int = 5


def extract_token_string(token_data: Any) -> Optional[str]:

    """
    Extract the actual token string from cached data, regardless of format.
    
    Handles nested tuples created by repeated wrapping:
    - Direct string: "eyJ0eXAi..."
    - Single tuple: ("eyJ0eXAi...", False)
    - Nested tuples: ((("eyJ0eXAi...", False), False), False)
    - Dict: {"token": "eyJ0eXAi...", "in_use": False}
    
    Accepts:
        * token_data (Any): Token data from cache (any format)
        
    Returns:
        * Optional[str]: The token string, or None if invalid
    """
    if token_data is None:
        return None
    
    # If it's already a string, validate and return it
    if isinstance(token_data, str):
        if token_data and token_data.startswith('eyJ'):
            return token_data
        else:
            LOGGER.warning(f"Token string doesn't look like JWT: {token_data[:30] if len(token_data) > 30 else token_data}...")
            return None
    
    # If it's a dict, extract the 'token' key
    if isinstance(token_data, dict):
        return extract_token_string(token_data.get('token'))
    
    # If it's a tuple, unwrap it recursively
    if isinstance(token_data, tuple):
        current = token_data
        depth = 0
        max_depth = 20  # Safety limit
        
        while isinstance(current, tuple) and depth < max_depth:
            if len(current) == 0:
                LOGGER.error("Empty tuple in token data")
                return None
            
            # Take the first element (the token)

            current = current[0]
            depth += 1
        
        if depth >= max_depth:
            LOGGER.error(f"Token nested too deeply (>{max_depth} levels)")
            return None
        
        if depth > 1:
            LOGGER.warning(f"Token was nested {depth} levels deep - fixed automatically")
        
        # Now we should have a string, recurse to validate
        return extract_token_string(current)
    
    # Unknown type
    LOGGER.error(f"Unexpected token data type: {type(token_data)}")
    return None


def is_token_expired(token: str, buffer_seconds: int = 300) -> bool:
    """
    Check if an Azure AD JWT token is expired or will expire soon.
    
    Accepts:
        * token (str): The JWT token to check
        * buffer_seconds (int): Consider token expired if it expires within this many seconds (default: 5 minutes)
        
    Returns:
        * bool: True if token is expired or will expire soon, False otherwise
    """
    if not token or not isinstance(token, str):
        LOGGER.warning("Invalid token provided to is_token_expired")
        return True
    
    try:
        # JWT format: header.payload.signature
        parts = token.split('.')
        if len(parts) != 3:
            LOGGER.warning("Token is not a valid JWT format (doesn't have 3 parts)")
            return True  # Treat as expired if malformed
        
        # Decode the payload (middle part)
        payload_part = parts[1]
        # Add padding if needed for base64 decoding
        padding = 4 - (len(payload_part) % 4)
        if padding != 4:
            payload_part += '=' * padding
        
        payload_bytes = base64.urlsafe_b64decode(payload_part)
        payload = json.loads(payload_bytes)
        
        # Get expiration time
        exp = payload.get('exp')
        if not exp:
            LOGGER.warning("Token has no expiration claim (exp)")
            return True  # Treat as expired if no exp claim
        

        # Check if expired (with buffer)
        current_time = time.time()
        time_until_expiry = exp - current_time
        
        if time_until_expiry <= buffer_seconds:
            LOGGER.warning(f"Token will expire in {time_until_expiry:.0f} seconds (buffer: {buffer_seconds}s)")
            return True
        
        LOGGER.debug(f"Token is valid for {time_until_expiry:.0f} more seconds")
        return False
        
    except Exception as exc:
        LOGGER.error(f"Error checking token expiration: {exc}")
        return True  # Treat as expired on error



def authenticate_with_azure(client_id: str, client_secret: str) -> bool:
    """
    Authenticate with Azure AD and cache the access token.
    
    Accepts:
        * client_id (str): Azure AD application client ID
        * client_secret (str): Azure AD application client secret
        
    Returns:
        * bool: True if authentication successful, False otherwise
    """
    url = f"https://login.microsoftonline.us/{AZURE_TENANT_ID}/oauth2/token"

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "resource": "https://high.analysis.usgovcloudapi.net/powerbi/api"
    } 
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    LOGGER.info(f"Authenticating with Azure - attempting to get new token") 

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        data = response.json()
        token = data["access_token"]
        token_expires_on = data["expires_on"]
        token_expires_in = data["expires_in"]
    except (requests.ConnectionError) as exc:
        LOGGER.error(f"Failed to authenticate with Azure and get new token: {exc}")
        return False
    except KeyError as exc:
        LOGGER.error(f"Token not found in Azure response: {exc}")
        LOGGER.error(f"Response: {response.text}")
        return False

    try:
        LOGGER.info(f"Caching token at: {AZURE_TOKEN_CACHE_KEY} for {AZURE_AUTH_CACHE_TIMEOUT} seconds")
        cache_azure_auth_tokens(token=token, expires_in=token_expires_in, expires_on=token_expires_on)
        LOGGER.info(f"Successfully cached token (length: {len(token)} chars) which expires on {token_expires_on}")
    except Exception as exc:
        LOGGER.error(f"Failed to cache token: {exc}")
        return False

    return True 


def cache_azure_auth_tokens(token: str, expires_in: int, expires_on: int) -> None:
    """
    Cache Azure AD access token.
    
    FIXED: Now stores ONLY the token string (no wrapping in tuples).
    This prevents the nested tuple bug.

    Accepts:
        * token (str): Azure AD access token
        * expires_in (int): Token expiration time in seconds
        * expires_on (int): Token expiration timestamp

    Returns:
        * None
    """
    # Extract clean token string in case it was somehow already wrapped
    clean_token = extract_token_string(token)
    
    if not clean_token:
        LOGGER.error("Failed to extract clean token string for caching")
        return
    
    # Store ONLY the token string - no tuples!
    cache.set(
        AZURE_TOKEN_CACHE_KEY,
        clean_token,  # Just the string, nothing else
        AZURE_AUTH_CACHE_TIMEOUT
    )

    cache.set(
        AZURE_TOKEN_CACHE_KEY_EXPIRES_IN,
        expires_in,
        AZURE_AUTH_CACHE_TIMEOUT
    )

    cache.set(
        AZURE_TOKEN_CACHE_KEY_EXPIRES_ON,
        expires_on,
        AZURE_AUTH_CACHE_TIMEOUT
    )
    
    LOGGER.debug(f"Cached clean token string (length: {len(clean_token)} chars)")


# ============================================================================
# TOKEN POOLING FUNCTIONS FOR CONCURRENT JOB SUPPORT
# ============================================================================

def get_powerbi_token_for_job() -> Tuple[str, Optional[str]]:
    """
    Retrieves an available Azure AD access token for PowerBI API calls.
    
    This function implements a token pooling mechanism to support concurrent
    export jobs. It maintains multiple tokens in cache, each marked as either
    'in use' or 'available'.
    
    FIXED: 
    - Now uses extract_token_string() to handle nested tuples
    - Checks token expiration before using cached tokens
    - Deletes expired tokens from cache
    
    The function will:
    1. Check the pool for an available token
    2. Extract clean token string and verify not expired
    3. If found and valid, return it
    4. If not found or expired, authenticate and create a new token
    5. Add it to the pool if space is available
    
    Accepts:
        * None
        
    Returns:
        * Tuple[str, Optional[str]]: A tuple containing:
            - token_cache_key (str): The cache key for this token
            - token (Optional[str]): The Azure AD access token string, or None
    """
    
    LOGGER.info("Searching for available PowerBI token for job execution...")
    
    # Check the main token first
    main_token_data = cache.get(AZURE_TOKEN_CACHE_KEY)
    if main_token_data:
        # Extract the actual token string (handles nested tuples)
        token_value = extract_token_string(main_token_data)
        
        if token_value:
            # Check if token is expired
            if not is_token_expired(token_value):
                # Check if there's an 'in_use' flag for main token
                in_use_key = f"{AZURE_TOKEN_CACHE_KEY}_in_use"
                in_use = cache.get(in_use_key, False)
                
                if not in_use:
                    LOGGER.info(f"Using main token: {AZURE_TOKEN_CACHE_KEY} (length: {len(token_value)} chars)")
                    return (AZURE_TOKEN_CACHE_KEY, token_value)
                else:
                    LOGGER.debug(f"Main token is in use, checking pool...")
            else:
                LOGGER.warning(f"Main token is expired, will get new one")
                cache.delete(AZURE_TOKEN_CACHE_KEY)
                cache.delete(f"{AZURE_TOKEN_CACHE_KEY}_in_use")
        else:
            LOGGER.warning(f"Main token exists but couldn't extract clean string")
            cache.delete(AZURE_TOKEN_CACHE_KEY)
    
    # Check the token pool
    for i in range(TOKEN_POOL_SIZE):
        token_cache_key = f"{AZURE_TOKEN_CACHE_KEY}_pool_{i}"
        token_data = cache.get(token_cache_key)
        
        if token_data:
            # Extract the actual token string
            token_value = extract_token_string(token_data)
            
            if token_value:
                # Check if token is expired
                if not is_token_expired(token_value):
                    # Check in_use flag (might be second element of tuple)
                    in_use = False
                    if isinstance(token_data, tuple) and len(token_data) > 1:
                        # Second element should be the in_use flag
                        in_use_value = token_data[1]

                        # Handle nested tuples in the flag too
                        while isinstance(in_use_value, tuple) and len(in_use_value) > 0:
                            in_use_value = in_use_value[0]
                        in_use = bool(in_use_value) if isinstance(in_use_value, bool) else False
                    
                    if not in_use:
                        LOGGER.info(f"Using pooled token {i}: {token_cache_key} (length: {len(token_value)} chars)")
                        return (token_cache_key, token_value)
                else:
                    LOGGER.warning(f"Pooled token {i} is expired, deleting")
                    cache.delete(token_cache_key)
            else:
                LOGGER.warning(f"Pooled token {i} exists but couldn't extract clean string")
                cache.delete(token_cache_key)
    
    # No available tokens found, need to authenticate
    LOGGER.info("No available tokens found. Authenticating with Azure AD...")
    
    try:
        # Authenticate with Azure
        success = authenticate_with_azure(
            client_id=AZURE_CLIENT_ID,
            client_secret=AZURE_CLIENT_SECRET
        )
        
        if not success:
            LOGGER.error("Failed to authenticate with Azure AD")
            return (AZURE_TOKEN_CACHE_KEY, None)
        
        # Get the newly created token
        new_token_data = cache.get(AZURE_TOKEN_CACHE_KEY)
        
        if not new_token_data:
            LOGGER.error("Token not found in cache after authentication")
            return (AZURE_TOKEN_CACHE_KEY, None)
        
        # Extract the clean token string
        new_token = extract_token_string(new_token_data)
        
        if not new_token:
            LOGGER.error("Newly acquired token is invalid or couldn't be extracted")
            return (AZURE_TOKEN_CACHE_KEY, None)
        
        # Verify new token is not expired
        if is_token_expired(new_token):
            LOGGER.error("Newly acquired token is already expired!")
            return (AZURE_TOKEN_CACHE_KEY, None)
        
        LOGGER.info(f"New token acquired (length: {len(new_token)} chars)")
        
        # Try to add to pool if space is available
        for i in range(TOKEN_POOL_SIZE):
            token_cache_key = f"{AZURE_TOKEN_CACHE_KEY}_pool_{i}"
            if not cache.get(token_cache_key):
                # Empty slot found, use it
                # Store as tuple: (token_string, in_use_flag)
                cache.set(
                    token_cache_key,
                    (new_token, False),  # Clean string + flag
                    AZURE_AUTH_CACHE_TIMEOUT
                )
                LOGGER.info(f"Created new token in pool slot {i}: {token_cache_key}")
                return (token_cache_key, new_token)
        
        # Pool is full, use main token
        LOGGER.info(f"Token pool full, using main token: {AZURE_TOKEN_CACHE_KEY}")
        return (AZURE_TOKEN_CACHE_KEY, new_token)
        
    except Exception as exc:
        LOGGER.error(f"Error during token acquisition: {exc}")
        import traceback
        LOGGER.error(traceback.format_exc())
        return (AZURE_TOKEN_CACHE_KEY, None)


def refresh_powerbi_token(token_cache_key: str) -> bool:
    """
    Refreshes an Azure AD access token.
    
    Azure AD tokens expire after 1 hour. This function re-authenticates
    to get a fresh token.
    
    FIXED: Now extracts clean token strings before re-caching.
    
    Accepts:
        * token_cache_key (str): The cache key of the token to refresh
        
    Returns:
        * bool: True if refresh successful, False otherwise
    """
    
    LOGGER.info(f"Refreshing PowerBI token: {token_cache_key}")
    
    try:
        # Get the current token data to check if it's in use
        current_data = cache.get(token_cache_key)
        in_use = False
        
        if isinstance(current_data, tuple) and len(current_data) > 1:
            # Extract in_use flag (second element)
            in_use_value = current_data[1]
            # Handle nested tuples in the flag
            while isinstance(in_use_value, tuple) and len(in_use_value) > 0:
                in_use_value = in_use_value[0]
            in_use = bool(in_use_value) if isinstance(in_use_value, bool) else False
        
        # Authenticate to get new token
        success = authenticate_with_azure(
            client_id=AZURE_CLIENT_ID,
            client_secret=AZURE_CLIENT_SECRET
        )
        
        if not success:
            LOGGER.error("Failed to refresh token: Authentication failed")
            return False
        
        # Get the new token from main cache
        new_token_data = cache.get(AZURE_TOKEN_CACHE_KEY)
        
        if not new_token_data:
            LOGGER.error("Failed to refresh token: Token not found after auth")
            return False
        
        # Extract clean token string
        new_token = extract_token_string(new_token_data)
        
        if not new_token:
            LOGGER.error("Failed to refresh token: Couldn't extract clean token")
            return False
        
        # Update the specific cache key with new token
        # Store as tuple: (clean_token_string, in_use_flag)
        cache.set(
            token_cache_key,
            (new_token, in_use),
            AZURE_AUTH_CACHE_TIMEOUT
        )
        
        LOGGER.info(f"Successfully refreshed token: {token_cache_key}")
        return True
        
    except Exception as exc:
        LOGGER.error(f"Error refreshing token: {exc}")
        return False


def release_powerbi_token(token_cache_key: str) -> None:
    """
    Marks a PowerBI token as no longer in use.
    
    This should be called when a job completes to make the token
    available for other jobs.
    
    FIXED: Now extracts clean token string before re-caching.
    
    Accepts:
        * token_cache_key (str): The cache key of the token to release
        
    Returns:
        * None
    """
    
    LOGGER.info(f"Releasing PowerBI token: {token_cache_key}")
    
    try:
        # If it's the main token, just clear the in_use flag
        if token_cache_key == AZURE_TOKEN_CACHE_KEY:
            in_use_key = f"{AZURE_TOKEN_CACHE_KEY}_in_use"
            cache.set(in_use_key, False, AZURE_AUTH_CACHE_TIMEOUT)
            LOGGER.info(f"Main token released: {token_cache_key}")
            return
        
        token_data = cache.get(token_cache_key)
        
        if token_data:
            # Extract clean token string (handles nested tuples)
            token_value = extract_token_string(token_data)
            
            if not token_value:
                LOGGER.warning(f"Token found but couldn't extract clean string: {token_cache_key}")
                cache.delete(token_cache_key)
                return
            
            # Mark as not in use - store as tuple: (clean_string, False)
            cache.set(
                token_cache_key,
                (token_value, False),
                AZURE_AUTH_CACHE_TIMEOUT
            )
            LOGGER.info(f"Token released: {token_cache_key}")
        else:
            LOGGER.warning(f"Token not found in cache: {token_cache_key}")
            
    except Exception as exc:
        LOGGER.error(f"Error releasing token: {exc}")


def cleanup_expired_tokens() -> int:
    """
    Removes expired tokens from the cache.
    
    This function can be called periodically to clean up the token pool.

    
    FIXED: Now properly checks JWT expiration using is_token_expired().
    
    Accepts:
        * None
        
    Returns:
        * int: Number of tokens cleaned up
    """
    
    LOGGER.info("Cleaning up expired PowerBI tokens...")
    
    cleaned_count = 0
    
    try:
        # Check main token
        main_token_data = cache.get(AZURE_TOKEN_CACHE_KEY)
        if main_token_data:
            token_string = extract_token_string(main_token_data)
            if not token_string or is_token_expired(token_string):
                cache.delete(AZURE_TOKEN_CACHE_KEY)
                cache.delete(f"{AZURE_TOKEN_CACHE_KEY}_in_use")
                cleaned_count += 1
                LOGGER.info("Cleaned up expired main token")
        
        # Check pool tokens
        for i in range(TOKEN_POOL_SIZE):
            token_cache_key = f"{AZURE_TOKEN_CACHE_KEY}_pool_{i}"
            token_data = cache.get(token_cache_key)
            
            if token_data:
                token_string = extract_token_string(token_data)
                if not token_string or is_token_expired(token_string):
                    cache.delete(token_cache_key)
                    cleaned_count += 1
                    LOGGER.info(f"Cleaned up expired pool token {i}")
        
        LOGGER.info(f"Cleaned up {cleaned_count} expired tokens")
        return cleaned_count
        
    except Exception as exc:
        LOGGER.error(f"Error during token cleanup: {exc}")
        return cleaned_count


def get_token_pool_status() -> dict:
    """
    Returns the status of the token pool.
    
    Useful for debugging and monitoring.
    
    FIXED: Now extracts clean tokens and checks expiration.
    
    Accepts:
        * None
        
    Returns:
        * dict: Status information about the token pool

    """
    
    status = {
        "main_token": None,
        "pool_tokens": [],
        "total_available": 0,
        "total_in_use": 0,
        "total_expired": 0
    }
    
    try:
        # Check main token
        main_token_data = cache.get(AZURE_TOKEN_CACHE_KEY)
        if main_token_data:
            in_use_key = f"{AZURE_TOKEN_CACHE_KEY}_in_use"
            in_use = cache.get(in_use_key, False)
            
            token_string = extract_token_string(main_token_data)
            is_expired = not token_string or is_token_expired(token_string)
            
            status["main_token"] = {
                "exists": True,
                "in_use": in_use,
                "has_value": bool(token_string),
                "is_expired": is_expired,
                "token_length": len(token_string) if token_string else 0
            }
            
            if is_expired:
                status["total_expired"] += 1
            elif in_use:
                status["total_in_use"] += 1
            else:
                status["total_available"] += 1
        else:
            status["main_token"] = {"exists": False}
            status["total_expired"] += 1
        
        # Check pool tokens
        for i in range(TOKEN_POOL_SIZE):
            token_cache_key = f"{AZURE_TOKEN_CACHE_KEY}_pool_{i}"
            token_data = cache.get(token_cache_key)
            
            if token_data:
                # Extract token and in_use flag
                token_string = extract_token_string(token_data)
                
                in_use = False
                if isinstance(token_data, tuple) and len(token_data) > 1:
                    in_use_value = token_data[1]
                    while isinstance(in_use_value, tuple) and len(in_use_value) > 0:
                        in_use_value = in_use_value[0]
                    in_use = bool(in_use_value) if isinstance(in_use_value, bool) else False
                
                is_expired = not token_string or is_token_expired(token_string)
                
                status["pool_tokens"].append({
                    "slot": i,
                    "exists": True,
                    "in_use": in_use,

                    "has_value": bool(token_string),
                    "is_expired": is_expired,
                    "token_length": len(token_string) if token_string else 0
                })
                
                if is_expired:
                    status["total_expired"] += 1
                elif in_use:
                    status["total_in_use"] += 1
                else:
                    status["total_available"] += 1
            else:
                status["pool_tokens"].append({
                    "slot": i,
                    "exists": False
                })
                status["total_expired"] += 1
        
        return status
        
    except Exception as exc:
        LOGGER.error(f"Error getting token pool status: {exc}")
        return status
