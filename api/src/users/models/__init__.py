""" 
Module that provides models, etc to extend
Django.contrib.auth.models.User
"""

from users.models.Role import Role
from users.models.Access import Access
from users.models.Segment import Segment
from users.models.Profile import Profile, create_user_profile, save_user_profile
