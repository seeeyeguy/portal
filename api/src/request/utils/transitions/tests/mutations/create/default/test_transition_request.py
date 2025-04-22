"""
Collection of pytests for Request Transitions create utils.
"""

from typing import cast, List, Union

from django.test import tag

from request import exceptions, models
from request.models.Request.serializers import RequestSerializer
from request.models.Stage.Stage import Stage


from manager.utils.tests import MultiDBTestCase


@tag(
    "utils",
    "request_app",
    "request_app.utils",
    "utils.TestTransitionRequest",
    "request_app.transition.utils.create",
    "transition.utils.create.default",
)
class TestTransitionRequest(MultiDBTestCase):
    """Test suite for Request Transition utils."""

    fixtures: List[str] = []

    def _validate_transitions(self, request: models.Request) -> Union[bool, None]:
        """Helper function to validate a series of transitions related to a `Request`."""

        record = RequestSerializer(request).data
        graph = record["transitions"]
        nodes = graph["nodes"]

        transition = nodes[str(graph["latest"])]

        while transition:
            current_stage = cast(int, transition["stage"]["level"])
            previous_transition = cast(int, transition["previous_transition"])
            previous_transition_key = str(previous_transition)
            valid_previous_stages = cast(
                List[int], Stage.StageLevels.ADJACENCY_LIST[str(current_stage)]
            )
            if not (
                previous_transition_key in nodes
                and cast(int, nodes[previous_transition_key]["stage"]["level"])
                in valid_previous_stages
            ):
                raise exceptions.RequestError("Invalid Transition Graph.", status=409)
            transition = nodes[previous_transition_key]
        return True

    @tag("utils.transition.transition_request_from_null_to_draft")
    def test_transition_request_from_null_to_draft(self) -> None:
        """Success Case: Transition a `Request` from `NULL` to `DRAFT`."""

    @tag("utils.transition.transition_request_from_draft_to_submitted")
    def test_transition_request_from_draft_to_submitted(self) -> None:
        """Success Case: Transition a `Request` from `DRAFT` to `SUBMITTED`."""

    @tag(
        "utils.transition.transition_request_from_submitted_to_approved_by_business_process_expert"
    )
    def test_transition_request_from_submitted_to_approved_by_business_process_expert(
        self,
    ) -> None:
        """Success Case: Transition a `Request` from `SUBMITTED` to
        `APPROVED BY BUSINESS PROCESS EXPERT`."""

    @tag("utils.transition.transition_request_from_submitted_to_revise")
    def test_transition_request_from_submitted_to_revise(self) -> None:
        """Success Case: Transition a `Request` from `SUBMITTED` to `REVISE`."""

    @tag(
        "utils.transition.transition_request_from_submitted_to_rejected_by_business_process_expert"
    )
    def test_transition_request_from_submitted_to_rejected_by_business_process_expert(
        self,
    ) -> None:
        """Success Case: Transition a `Request` from `SUBMITTED` to
        `REJECTED BY BUSINESS PROCESS EXPERT`."""

    @tag("utils.transition.transition_request_from_submitted_to_approved_by_superuser")
    def test_transition_request_from_submitted_to_approved_by_superuser(self) -> None:
        """Success Case: Transition a `Request` from `SUBMITTED` to `APPROVED BY SUPERUSER`."""

    @tag("utils.transition.transition_request_from_submitted_to_rejected_by_superuser")
    def test_transition_request_from_submitted_to_rejected_by_superuser(self) -> None:
        """Success Case: Transition a `Request` from `SUBMITTED` to `REJECTED BY SUPERUSER`."""

    @tag("utils.transition.transition_request_from_submitted_revise_to_draft")
    def test_transition_request_from_submitted_revise_to_draft(
        self,
    ) -> None:
        """Success Case: Transition a `Request` from `SUBMITTED` to `REVISE` to `DRAFT`."""

    @tag(
        "utils.transition.transition_request_from_approved_by_bpe_to_approved_by_superuser"
    )
    def test_transition_request_from_approved_by_bpe_to_approved_by_superuser(
        self,
    ) -> None:
        """Success Case: Transition a `Request` from `APPROVED BY BUSINESS PROCESS EXPERT`
        to `APPROVED BY SUPERUSER`."""

    @tag("utils.transition.transition_request_from_approved_by_bpe_to_revise")
    def test_transition_request_from_approved_by_bpe_to_revise(self) -> None:
        """Success Case: Transition a `Request` from `APPROVED BY BUSINESS PROCESS EXPERT`
        to `REVISE`"""

    @tag(
        "utils.transition.transition_request_from_approved_by_bpe_to_rejected_by_superuser"
    )
    def test_transition_request_from_approved_by_bpe_to_rejected_by_superuser(
        self,
    ) -> None:
        """Success Case: Transition a `Request` from `APPROVED BY BUSINESS PROCESS EXPERT`
        to `REJECTED BY SUPERUSER`."""

    @tag("utils.transition.transition_request_from_approved_by_bpe_revise_to_draft")
    def test_transition_request_from_approved_by_bpe_revise_to_draft(self) -> None:
        """Success Case: Transition a `Request` from `APPROVED BY BUSINESS PROCESS OWNER` to
        `REVISE` to `DRAFT`."""

    @tag("utils.transition.transition_request_from_rejected_by_business_process_owner")
    def test_transition_request_from_rejected_by_business_process_owner(self) -> None:
        """Fail Case: Transition a `Request` from `REJECTED BY BUSINESS PROCESS OWNER`."""

    @tag("utils.transition.transition_request_from_approved_by_superuser")
    def test_transition_request_from_approved_by_superuser(self) -> None:
        """Fail Case: Transition a `Request` from `APPROVED BY SUPERUSER`."""

    @tag("utils.transition.transition_request_from_rejected_by_superuser")
    def test_transition_request_from_rejected_by_superuser(self) -> None:
        """Fail Case: Transition a `Request` from `REJECTED BY SUPERUSER`."""
