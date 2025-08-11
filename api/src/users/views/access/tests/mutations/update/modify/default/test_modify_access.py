"""
Collection of pytests for Access's modify update view endpoint.
"""

from typing import List

from django.contrib.auth import models as AuthModels
from django.test import tag
from django.urls import reverse
from rest_framework import status

from users.views.access.tests.mutations.update.modify.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

from manager.utils.tests import MultiDBTestCase


@tag(
    "users",
    "access",
    "views",
    "users.access.update.modify",
    "users.access.update",
    "access.update.default",
    "views.TestModifyAccess",
)
class TestModifyAccess(MultiDBTestCase):
    """
    Tests for PUT /v1/users/access/subfunctions endpoint.
    """

    def setUp(self) -> None:

        super().setUp()
        user = AuthModels.User.objects.get(
            email=arguments.MODIFY_ACCESS_ADMIN_USER_EMAIL
        )
        self.client.force_login(user=user)

    fixtures: List[str] = [*COMMON_FIXTURES]

    url: str = reverse("users.access.subfunctions")

    @tag("views.access.modify_access")
    def test_modify_access(self) -> None:
        """Success Case: Modify an `Access` record, given its id
        and a collection of subfunctions."""

        request_url = f"{self.url}?id={arguments.MODIFY_ACCESS_ACCESS_ID}"

        body = {"subfunctions": arguments.MODIFY_ACCESS_SUBFUNCTIONS}

        response = self.client.put(request_url, body, content_type="application/json")

        access = response.json()
        permitted_subfunctions = list(
            map(lambda record: record["id"], access.pop("subfunctions"))
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            len(permitted_subfunctions), len(arguments.MODIFY_ACCESS_SUBFUNCTIONS)
        )

        for subfunction_id in arguments.MODIFY_ACCESS_SUBFUNCTIONS:
            self.assertIn(subfunction_id, permitted_subfunctions)
