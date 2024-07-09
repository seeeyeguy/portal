"""
Routing module for LDAP, providing a list
of urlpatterns for a request to the LDAP
service.
"""

from django.urls import path

from manager.services.ldap import views
from manager.settings import ApplicationServices


urlpatterns = [
    path(
        f"{ApplicationServices.SERVICE_PATH_PREFIX}/ldap",
        view=views.LDAPSearch.as_view(),
        name="ldap-search",
    )
]
