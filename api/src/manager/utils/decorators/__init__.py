"""
Decorator module. This module provides several
decorators that help our application process
requests and keep code DRY.
"""

from manager.utils.decorators.views import (
    admin_required,
    login_required,
    with_serializer,
)
