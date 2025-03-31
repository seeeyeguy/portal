"""
Tests util module. This module provide common functionality
that may be used for tests across the project.
"""

from django.test import TestCase


class MultiDBTestCase(TestCase):
    """`TestCase` subclass to handle tests within multi-db architecture."""

    databases = {"default", "prt"}
