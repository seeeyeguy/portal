""" 
BI Portal `Directory` admin module. We register `Directory` app
models with the Django admin site here.
"""

from typing import Any

from django.contrib import admin
from django.http.request import HttpRequest

from directory import models


class ResourceAdmin(admin.ModelAdmin):
    """Admin panel specification for `Resource` data."""

    model = models.Resource

    actions = None
    fields = ["name", "description", "url", "thumbnail"]
    ordering = ["id"]
    readonly_fields = ["name", "description", "url"]
    search_fields = ["name", "uid"]

    def has_add_permission(self, _: HttpRequest) -> bool:
        """Determine whether a record may be added by an admin."""

        return False

    def has_delete_permission(self, _: HttpRequest, __: Any | None = ...) -> bool:
        """Determine whether a record may be deleted by an admin."""

        return False


admin.site.register(models.Resource, ResourceAdmin)
