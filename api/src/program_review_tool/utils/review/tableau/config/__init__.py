"""
Config module to configure settings to connect to
the L3Harris Tableau server.
"""

import os

TABLEAU_API_VERSION: str = "3.13"
TABLEAU_CA_CERTIFICATE: str = os.getenv("TABLEAU_CA_CERTIFICATE", "")
TABLEAU_PERSONAL_ACCESS_TOKEN_NAME: str = os.getenv(
    "TABLEAU_PERSONAL_ACCESS_TOKEN_NAME", "prt"
)
TABLEAU_PERSONAL_ACCESS_TOKEN_SECRET: str = os.getenv(
    "TABLEAU_PERSONAL_ACCESS_TOKEN_SECRET", "secret-key"
)
TABLEAU_SERVER: str = os.getenv("TABLEAU_SERVER", "https://tableau.l3harris.com")
