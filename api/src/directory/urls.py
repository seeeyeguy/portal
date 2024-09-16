"""
URLpatterns provides endpoints as a gateway between the server and
the client, where they can interact with the `Directory` API, participating
in the request/response cycle.
"""

from django.urls import path

from directory import views

from manager.utils.types import urlconfig

urlpatterns: urlconfig.PathPatternList = [
    path(
        "resources/search",
        view=views.ResourceSearch.as_view(),
        name="directory.resource.search",
    ),
    path(
        "employee-levels",
        view=views.EmployeeLevel.as_view(),
        name="directory.employeelevel",
    ),
    path(
        "functions",
        view=views.Function.as_view(),
        name="directory.function",
    ),
    path(
        "subfunctions",
        view=views.SubFunction.as_view(),
        name="directory.subfunction",
    ),
    path(
        "tags",
        view=views.Tag.as_view(),
        name="directory.tag",
    ),
    path("tags/search", view=views.TagSearch.as_view(), name="directory.tag.search"),
]
