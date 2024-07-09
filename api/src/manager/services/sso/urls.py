"""
Routing module for SSO, providing a list
of urlpatterns for a request to the SSO
service.
"""

from django.urls import path

from manager.services.sso import views
from manager.settings import ApplicationServices

urlpatterns = [
    path(
        f"{ApplicationServices.SERVICE_PATH_PREFIX}/sso/<str:auth>",
        view=views.Login.as_view(),
        name="sso-login",
    ),
    path(
        f"{ApplicationServices.SERVICE_PATH_PREFIX}/sso/logout",
        view=views.Logout.as_view(),
        name="sso-logout",
    ),
    path(
        f"{ApplicationServices.SERVICE_PATH_PREFIX}/sso/user",
        view=views.AuthenticatedUser.as_view(),
        name="sso-fetch-user",
    ),
]
