"""
Collection of pytests for Request Transitions create utils.
"""

import pytest
from typing import cast, List, Union

from django.test import tag

from request import exceptions, models
from request.models.Request.serializers import RequestSerializer
from request.models.Stage.Stage import Stage
from request.utils.transitions import transition_request
from request.utils.transitions.tests.mutations.create.default import arguments

from portal.models.fixtures import COMMON_FIXTURES

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

    fixtures: List[str] = [
        *COMMON_FIXTURES,
        "request/utils/transitions/tests/mutations/create/default/fixtures/resources.json",
        "request/utils/transitions/tests/mutations/create/default/fixtures/requests.json",
        "request/utils/transitions/tests/mutations/create/default/fixtures/transitions.json",
        "request/utils/transitions/tests/mutations/create/default/fixtures/dispositions.json",
    ]

    def _validate_transitions(self, request: models.Request) -> Union[bool, None]:
        """Helper function to validate a series of transitions related to a `Request`."""

        record = RequestSerializer(request).data
        graph = record["transitions"]
        nodes = graph["nodes"]

        transition = nodes[str(graph["latest"])]

        while transition:
            current_stage = cast(int, transition["stage"]["level"])
            previous_transition = (
                cast(int, transition["previous_transition"])
                if current_stage != Stage.StageLevels.DRAFT
                else None
            )
            previous_transition_key = str(previous_transition)
            valid_previous_stages = cast(
                List[int], Stage.StageLevels.ADJACENCY_LIST[str(current_stage)]
            )
            if not (
                previous_transition is None
                or previous_transition_key in nodes
                and cast(int, nodes[previous_transition_key]["stage"]["level"])
                in valid_previous_stages
            ):
                raise exceptions.RequestError("Invalid Transition Graph.", status=409)
            transition = nodes[previous_transition_key] if previous_transition else None
        return True

    @tag("utils.transition.transition_request_from_null_to_draft")
    def test_transition_request_from_null_to_draft(self) -> None:
        """Success Case: Transition a `Request` from `NULL` to `DRAFT`."""

        request, transition = transition_request(
            request_id=arguments.REQUEST_ID_AT_NULL_STAGE
        )
        self.assertEqual(transition.stage.level, models.Stage.StageLevels.DRAFT)
        self.assertTrue(self._validate_transitions(request=request))

    @tag("utils.transition.transition_request_from_draft_to_submitted")
    def test_transition_request_from_draft_to_submitted(self) -> None:
        """Success Case: Transition a `Request` from `DRAFT` to `SUBMITTED`."""

        request, transition = transition_request(
            request_id=arguments.REQUEST_ID_AT_DRAFT_STAGE
        )
        self.assertEqual(transition.stage.level, models.Stage.StageLevels.SUBMITTED)
        self.assertTrue(self._validate_transitions(request=request))

    @tag(
        "utils.transition.transition_request_from_submitted_to_approved_by_business_process_expert"
    )
    def test_transition_request_from_submitted_to_approved_by_business_process_expert(
        self,
    ) -> None:
        """Success Case: Transition a `Request` from `SUBMITTED` to
        `APPROVED BY BUSINESS PROCESS EXPERT`."""

        request, transition = transition_request(
            request_id=arguments.REQUEST_ID_AT_SUBMITTED_STAGE[
                "APPROVED BY BUSINESS PROCESS EXPERT"
            ]
        )
        self.assertEqual(
            transition.stage.level,
            models.Stage.StageLevels.APPROVED_BY_BUSINESS_PROCESS_EXPERT,
        )
        self.assertTrue(self._validate_transitions(request=request))

    @tag("utils.transition.transition_request_from_submitted_to_revise")
    def test_transition_request_from_submitted_to_revise(self) -> None:
        """Success Case: Transition a `Request` from `SUBMITTED` to `REVISE`."""

        request, transition = transition_request(
            request_id=arguments.REQUEST_ID_AT_SUBMITTED_STAGE["REVISE"]
        )
        self.assertEqual(transition.stage.level, models.Stage.StageLevels.REVISE)
        self.assertTrue(self._validate_transitions(request=request))

    @tag(
        "utils.transition.transition_request_from_submitted_to_rejected_by_business_process_expert"
    )
    def test_transition_request_from_submitted_to_rejected_by_business_process_expert(
        self,
    ) -> None:
        """Success Case: Transition a `Request` from `SUBMITTED` to
        `REJECTED BY BUSINESS PROCESS EXPERT`."""

        request, transition = transition_request(
            request_id=arguments.REQUEST_ID_AT_SUBMITTED_STAGE[
                "REJECTED BY BUSINESS PROCESS EXPERT"
            ]
        )
        self.assertEqual(
            transition.stage.level,
            models.Stage.StageLevels.REJECTED_BY_BUSINESS_PROCESS_EXPERT,
        )
        self.assertTrue(self._validate_transitions(request=request))

    @tag("utils.transition.transition_request_from_submitted_to_approved_by_superuser")
    def test_transition_request_from_submitted_to_approved_by_superuser(self) -> None:
        """Success Case: Transition a `Request` from `SUBMITTED` to `APPROVED BY SUPERUSER`."""

        request, transition = transition_request(
            request_id=arguments.REQUEST_ID_AT_SUBMITTED_STAGE["APPROVED BY SUPERUSER"]
        )
        self.assertEqual(
            transition.stage.level, models.Stage.StageLevels.APPROVED_BY_SUPERUSER
        )
        self.assertTrue(self._validate_transitions(request=request))

    @tag("utils.transition.transition_request_from_submitted_to_rejected_by_superuser")
    def test_transition_request_from_submitted_to_rejected_by_superuser(self) -> None:
        """Success Case: Transition a `Request` from `SUBMITTED` to `REJECTED BY SUPERUSER`."""

        request, transition = transition_request(
            request_id=arguments.REQUEST_ID_AT_SUBMITTED_STAGE["REJECTED BY SUPERUSER"]
        )
        self.assertEqual(
            transition.stage.level, models.Stage.StageLevels.REJECTED_BY_SUPERUSER
        )
        self.assertTrue(self._validate_transitions(request=request))

    @tag("utils.transition.transition_request_from_submitted_revise_to_draft")
    def test_transition_request_from_submitted_revise_to_draft(
        self,
    ) -> None:
        """Success Case: Transition a `Request` from `SUBMITTED` to `REVISE` to `DRAFT`."""

        request, transition = transition_request(
            request_id=arguments.REQUEST_ID_AT_SUBMITTED_STAGE["REVISE"]
        )
        self.assertEqual(transition.stage.level, models.Stage.StageLevels.REVISE)
        request, transition = transition_request(request_id=request.id)
        self.assertEqual(transition.stage.level, models.Stage.StageLevels.DRAFT)
        self.assertTrue(self._validate_transitions(request=request))

    @tag(
        "utils.transition.transition_request_from_approved_by_bpe_to_approved_by_superuser"
    )
    def test_transition_request_from_approved_by_bpe_to_approved_by_superuser(
        self,
    ) -> None:
        """Success Case: Transition a `Request` from `APPROVED BY BUSINESS PROCESS EXPERT`
        to `APPROVED BY SUPERUSER`."""

        request, transition = transition_request(
            request_id=arguments.REQUEST_ID_AT_APPROVED_BY_BUSINESS_PROCESS_EXPERT_STAGE[
                "APPROVED BY SUPERUSER"
            ]
        )
        self.assertEqual(
            transition.stage.level, models.Stage.StageLevels.APPROVED_BY_SUPERUSER
        )
        self.assertTrue(self._validate_transitions(request=request))

    @tag("utils.transition.transition_request_from_approved_by_bpe_to_revise")
    def test_transition_request_from_approved_by_bpe_to_revise(self) -> None:
        """Success Case: Transition a `Request` from `APPROVED BY BUSINESS PROCESS EXPERT`
        to `REVISE`"""

        request, transition = transition_request(
            request_id=arguments.REQUEST_ID_AT_APPROVED_BY_BUSINESS_PROCESS_EXPERT_STAGE[
                "REVISE"
            ]
        )
        self.assertEqual(transition.stage.level, models.Stage.StageLevels.REVISE)
        self.assertTrue(self._validate_transitions(request=request))

    @tag(
        "utils.transition.transition_request_from_approved_by_bpe_to_rejected_by_superuser"
    )
    def test_transition_request_from_approved_by_bpe_to_rejected_by_superuser(
        self,
    ) -> None:
        """Success Case: Transition a `Request` from `APPROVED BY BUSINESS PROCESS EXPERT`
        to `REJECTED BY SUPERUSER`."""

        request, transition = transition_request(
            request_id=arguments.REQUEST_ID_AT_APPROVED_BY_BUSINESS_PROCESS_EXPERT_STAGE[
                "REJECTED BY SUPERUSER"
            ]
        )
        self.assertEqual(
            transition.stage.level, models.Stage.StageLevels.REJECTED_BY_SUPERUSER
        )
        self.assertTrue(self._validate_transitions(request=request))

    @tag("utils.transition.transition_request_from_approved_by_bpe_revise_to_draft")
    def test_transition_request_from_approved_by_bpe_revise_to_draft(self) -> None:
        """Success Case: Transition a `Request` from `APPROVED BY BUSINESS PROCESS EXPERT` to
        `REVISE` to `DRAFT`."""

        request, transition = transition_request(
            request_id=arguments.REQUEST_ID_AT_APPROVED_BY_BUSINESS_PROCESS_EXPERT_STAGE[
                "REVISE"
            ]
        )
        self.assertEqual(transition.stage.level, models.Stage.StageLevels.REVISE)
        request, transition = transition_request(request_id=request.id)
        self.assertEqual(transition.stage.level, models.Stage.StageLevels.DRAFT)
        self.assertTrue(self._validate_transitions(request=request))

    @tag("utils.transition.transition_request_from_rejected_by_business_process_expert")
    def test_transition_request_from_rejected_by_business_process_expert(self) -> None:
        """Fail Case: Transition a `Request` from `REJECTED BY BUSINESS PROCESS EXPERT`."""

        with pytest.raises(exceptions.RequestError):
            _ = transition_request(
                request_id=arguments.REQUEST_ID_AT_REJECTED_BY_BUSINESS_PROCESS_EXPERT_STAGE
            )

    @tag("utils.transition.transition_request_from_approved_by_superuser")
    def test_transition_request_from_approved_by_superuser(self) -> None:
        """Fail Case: Transition a `Request` from `APPROVED BY SUPERUSER`."""

        with pytest.raises(exceptions.RequestError):
            _ = transition_request(
                request_id=arguments.REQUEST_ID_AT_APPROVED_BY_SUPERUSER_STAGE
            )

    @tag("utils.transition.transition_request_from_rejected_by_superuser")
    def test_transition_request_from_rejected_by_superuser(self) -> None:
        """Fail Case: Transition a `Request` from `REJECTED BY SUPERUSER`."""

        with pytest.raises(exceptions.RequestError):
            _ = transition_request(
                request_id=arguments.REQUEST_ID_AT_REJECTED_BY_SUPERUSER_STAGE
            )

    @tag("utils.transition.transition_request_request_dne")
    def test_transition_request_request_dne(self) -> None:
        """Fail Case: Transition a `Request` that does not exist."""

        with pytest.raises(exceptions.RequestError):
            _ = transition_request(request_id=arguments.REQUEST_ID_DNE)

    @tag("utils.transition.transition_request_request_not_pending")
    def test_transition_request_request_not_pending(self) -> None:
        """Fail Case: Transition a `Request` with an `APPROVED` status."""

        with pytest.raises(exceptions.RequestError):
            _ = transition_request(request_id=arguments.REQUEST_ID_REQUEST_APPROVED)
