"""
Routing module for built-in services, including urlpatterns
for SSO, LDAP, etc. 
"""

from manager.services.ldap import urls as LDAP_URLS
from manager.services.sso import urls as SSO_URLS

urlpatterns = [
    *LDAP_URLS.urlpatterns,
    *SSO_URLS.urlpatterns,
]
