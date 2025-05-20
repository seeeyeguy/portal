"""
Config module to configure settings to create
the `Program` review exports. Settings here
reference the directories used when generating exports
(EXPORT_DIR), and copying assets (ASSETS_DIR).
"""

import os

from manager.settings import BASE_DIR, MEDIA_ROOT

ASSETS_DIR = os.path.join(BASE_DIR, "program_review_tool/utils/review/export/assets")
EXPORT_DIR = os.path.join(MEDIA_ROOT, "export")
