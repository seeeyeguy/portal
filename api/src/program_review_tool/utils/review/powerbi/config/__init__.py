"""
Config module for powerbi settings to connect to the L3Harris PowerBI API
"""

import os


AZURE_POWERBI_URI: str = os.getenv("AZURE_POWERBI_URI", "") 
AZURE_CLIENT_ID: str = os.getenv("AZURE_CLIENT_ID", "")
AZURE_TENANT_ID: str = os.getenv("AZURE_TENANT_ID", "")
AZURE_SHARED_SECRET_ID: str = os.getenv("AZURE_SHARED_SECRET_ID", "")
AZURE_CLIENT_SECRET: str = os.getenv("AZURE_CLIENT_SECRET", "")
AZURE_TOKEN_CACHE_KEY: str = os.getenv("AZURE_TOKEN_CACHE_KEY", "")
AZURE_TOKEN_CACHE_KEY_EXPIRES_IN: str = os.getenv("AZURE_TOKEN_CACHE_KEY_EXPIRES_IN", "") 
AZURE_TOKEN_CACHE_KEY_EXPIRES_ON: str = os.getenv("AZURE_TOKEN_CACHE_KEY_EXPIRES_ON", "")

