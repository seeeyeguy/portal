"""
`BI Portal` `Access` view module. Views handle
requests to create, fetch, and update records
within the `Access` table. An `Access` represents
an individual access within the system associated
with a role. An `Access` conveys permissions to a
`User`, specifically the ability to submit a `Request`
and a `Disposition` for the appropriate `SubFunction`s
and `Stage`s. Only a `Superuser` may create, fetch, or
revoke `Access` records.
"""

import logging
from typing import List, Union

from django import http
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from rest_framework import status

from users import controllers, exceptions
from users.models.Access.serializers import AccessSerializer
from users.views import serializers

from manager.utils.decorators import login_required, with_serializer
from manager.utils.types.request import DjangoHttpRequest

LOGGER = logging.getLogger(__name__)


@method_decorator(never_cache, name="dispatch")
class Access(View):
    """
    Handle user requests to create, fetch, or update `Access`
    records for `BI Portal`. `Access` represents an individual
    access within the system associated with a role. An `Access`
    conveys permissions to a `User`, specifically the ability to
    submit a `Request` and a `Disposition` for the appropriate
    `SubFunction`s and `Stage`s. Only a `Superuser` may create,
    fetch, or revoke `Access` records.
    """

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.CreateAccessRequest))
    def post(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for POST /v1/users/access."""

        try:
            LOGGER.info("POST /v1/users/access.")

            # Create `Access` record.
            access_record = controllers.Access.create_access(
                user=body["user"],
                role_level=body["role_level"],
                subfunctions=body["subfunctions"],
                stage_levels=body["stage_levels"],
                admin=request.user,
            )

            # Serialize `Access` record.
            data: dict = AccessSerializer(access_record).data

            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
        except exceptions.UsersError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    def put(self, request: DjangoHttpRequest) -> http.JsonResponse:
        """Endpoint for PUT /v1/users/access."""

        try:
            req = serializers.RevokeAccessRequestQueryParams(data=request.GET)
            if not req.is_valid():
                return http.JsonResponse(
                    req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
                )

            access_ids: List[int] = req.validated_data.get("ids")

            log_msg = f"PUT /v1/users/access?ids={access_ids}."

            LOGGER.info(log_msg)

            # Revoke `Access` records.
            access_records, _ = controllers.Access.revoke_accesses(
                accesses=access_ids, admin=request.user
            )

            # Serialize `Access` records.
            data: dict = AccessSerializer(access_records, many=True).data

            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)
        except exceptions.UsersError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.FetchAccessRequest))
    def get(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for GET /v1/users/access."""

        try:
            log_msg = (
                f"GET /v1/users/access?id={body['id']}",
                f"&user={body['user']}&role_levels={body['role_levels']}"
                f"&subfunctions={body['subfunctions']}&include_revoked={body['include_revoked']}",
            )
            LOGGER.info(log_msg)

            # Fetch `Access` records.
            access_records = controllers.Access.fetch_accesses(
                access=body["id"],
                user=body["user"],
                role_levels=body["role_levels"],
                subfunctions=body["subfunctions"],
                include_revoked=body["include_revoked"],
                admin=request.user,
            )

            many: bool = body["id"] is None

            # Serialize `Access` record(s).
            data: Union[dict, List[dict]] = AccessSerializer(
                access_records, many=many
            ).data

            return http.JsonResponse(data, status=status.HTTP_200_OK, safe=False)
        except exceptions.UsersError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)


@method_decorator(never_cache, name="dispatch")
class AccessControl(View):
    """
    Handle user requests to update `Access` records for `BI Portal`.
    Here, we are specifically managing permissions in relation to
    `SubFunction`s. It is important to note that we will not be
    directly updating any record here. Instead, we will perform a
    "soft" update, whereby we will revoke the previous record and
    create a new record with the updated permissions.
    """

    @method_decorator(login_required())
    @method_decorator(with_serializer(serializers.UpdateAccessRequest))
    def put(self, request: DjangoHttpRequest, body: dict) -> http.JsonResponse:
        """Endpoint for PUT /v1/users/access/subfunctions."""

        try:
            req = serializers.UpdateAccessRequestQueryParams(data=request.GET)
            if not req.is_valid():
                return http.JsonResponse(
                    req.errors, status=status.HTTP_400_BAD_REQUEST, safe=False
                )

            access_id: int = req.validated_data.get("id")

            log_msg = f"PUT /v1/users/access/subfunctions?id={access_id}."

            LOGGER.info(log_msg)

            # Update `Access` record subfunctions.
            access_record, _ = controllers.Access.modify_access(
                access=access_id, subfunctions=body["subfunctions"], admin=request.user
            )

            # Serialize `Access` record.
            data: dict = AccessSerializer(access_record).data

            return http.JsonResponse(data, status=status.HTTP_201_CREATED, safe=False)

        except exceptions.UsersError as exc:
            LOGGER.error(exc.message)
            return http.JsonResponse(exc.message, status=exc.status, safe=False)
