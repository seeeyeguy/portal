"""
URLpatterns provides endpoints as a gateway between the server and
the client, where they can interact with the `Users` API, participating
in the request/response cycle.
"""

from django.urls import path

from users import views

from manager.utils.types import urlconfig

urlpatterns: urlconfig.PathPatternList = [
    path(
        "access",
        view=views.Access.as_view(),
        name="users.access",
    ),
    path(
        "access/subfunctions",
        view=views.AccessControl.as_view(),
        name="users.access.subfunctions",
    ),
    path(
        "profile",
        view=views.Profile.as_view(),
        name="users.profile",
    ),
]
