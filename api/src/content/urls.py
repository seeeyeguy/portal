"""
URLpatterns provides endpoints as a gateway between the server and
the client, where they can interact with the `Content` API, participating
in the request/response cycle.
"""

from django.urls import path

from content import views

from manager.utils.types import urlconfig

urlpatterns: urlconfig.PathPatternList = [
    path("content", view=views.Content.as_view(), name="content.content"),
]
