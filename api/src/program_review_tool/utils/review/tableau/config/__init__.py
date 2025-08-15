"""
Config module to configure settings to connect to
the L3Harris Tableau server.
"""

import json
import os

TABLEAU_API_VERSION: str = "3.13"
TABLEAU_CA_CERTIFICATE: str = os.getenv("TABLEAU_CA_CERTIFICATE", "")
TABLEAU_PERSONAL_ACCESS_TOKENS: dict = (
    json.loads(os.getenv("TABLEAU_PERSONAL_ACCESS_TOKENS", "{}"))
    if os.getenv("TABLEAU_PERSONAL_ACCESS_TOKENS", "")
    else {}
)

TABLEAU_SERVER: str = os.getenv("TABLEAU_SERVER", "https://tableau.l3harris.com")
