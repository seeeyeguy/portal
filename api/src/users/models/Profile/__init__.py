"""
`Profile` module. `Profile` extends the `User` model with
insightful data queried from LDAP.
"""

from users.models.Profile.Profile import Profile
from users.models.Profile.signals import create_user_profile, save_user_profile
