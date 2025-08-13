import pytest
from integration import ObjectKind
from port_ocean.context.ocean import PortOceanContext
from port_ocean.core.handlers.webhook.webhook_event import WebhookEvent, EventPayload
from tests.webhook_processors.test_base_webhook_processor import (
    BaseWebhookProcessorTest,
    mock_event,
    mock_context,
)
from webhook_processors.internal_incident_webhook_processor import (
    InternalSecretIncidentWebhookProcessor,
)


@pytest.fixture
def internal_incident_processor(
    mock_event: WebhookEvent,
) -> InternalSecretIncidentWebhookProcessor:
    return InternalSecretIncidentWebhookProcessor(mock_event)


class TestInternalSecretIncidentWebhookProcessor(BaseWebhookProcessorTest):
    __test__ = True

    @pytest.mark.asyncio
    async def test_should_process_event_valid_signature_and_timestamp(
        self,
        internal_incident_processor: InternalSecretIncidentWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        await super().test_should_process_event_valid_signature_and_timestamp(
            internal_incident_processor, mock_context
        )

    @pytest.mark.asyncio
    async def test_should_process_event_invalid_signature(
        self,
        internal_incident_processor: InternalSecretIncidentWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        await super().test_should_process_event_invalid_signature(
            internal_incident_processor, mock_context
        )

    @pytest.mark.asyncio
    async def test_should_process_event_with_unsupported_hash(
        self,
        internal_incident_processor: InternalSecretIncidentWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        await super().test_should_process_event_with_unsupported_hash(
            internal_incident_processor, mock_context
        )

    @pytest.mark.asyncio
    async def test_authenticate_with_expected_config_and_headers(
        self,
        internal_incident_processor: InternalSecretIncidentWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        await super().test_authenticate_with_expected_config_and_headers(
            internal_incident_processor, mock_context
        )

    @pytest.mark.asyncio
    async def test_authenticate_with_expected_config_and_no_headers(
        self,
        internal_incident_processor: InternalSecretIncidentWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        await super().test_authenticate_with_expected_config_and_no_headers(
            internal_incident_processor, mock_context
        )

    @pytest.mark.asyncio
    async def test_authenticate_with_expected_headers_and_no_config(
        self,
        internal_incident_processor: InternalSecretIncidentWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        await super().test_authenticate_with_expected_headers_and_no_config(
            internal_incident_processor, mock_context
        )

    @pytest.mark.asyncio
    async def test_get_matching_kinds(
        self,
        internal_incident_processor: InternalSecretIncidentWebhookProcessor,
    ) -> None:
        event = WebhookEvent(trace_id="test-trace-id", payload={}, headers={})
        result = await internal_incident_processor.get_matching_kinds(event)

        assert result == [ObjectKind.INTERNAL_SECRET_INCIDENT]

    @pytest.mark.asyncio
    async def test_validate_payload_with_incident_action(
        self,
        internal_incident_processor: InternalSecretIncidentWebhookProcessor,
    ) -> None:
        payload = self._get_mocked_assign_event_payload()
        result = await internal_incident_processor.validate_payload(payload=payload)

        assert result is True

    @pytest.mark.asyncio
    async def test_validate_payload_with_no_incident_action(
        self,
        internal_incident_processor: InternalSecretIncidentWebhookProcessor,
    ) -> None:
        payload = {"action": "some_other_action"}
        result = await internal_incident_processor.validate_payload(payload=payload)

        assert result is False

    def _get_mocked_assign_event_payload(self) -> EventPayload:
        return {
            "source": "GitGuardian",
            "timestamp": "2022-06-17T12:18:41.917977Z",
            "action": "incident_assigned",
            "message": "This incident has been assigned to a user.",
            "target_user": "John Doe john.doe@gitguardian.com",
            "target_team": "My team",
            "custom_webhook_name": "My custom webhook name",
            "incident": {
                "id": 31450,
                "date": "2022-06-15T09:16:42.378417Z",
                "detector": {
                    "name": "generic_password",
                    "display_name": "Generic Password",
                    "nature": "generic",
                    "family": "Other",
                    "detector_group_name": "generic_password",
                    "detector_group_display_name": "Generic Password",
                },
                "secret_hash": "xxx",
                "hmsl_hash": "xxx",
                "secret_revoked": False,
                "validity": "no_checker",
                "occurrence_count": 1,
                "status": "assigned",
                "declarative_secret_status": "active",
                "regression": False,
                "assignee_email": "bruce.wayne@gitguardian.com",
                "severity": "medium",
                "ignored_at": None,
                "ignore_reason": None,
                "resolved_at": None,
                "gitguardian_url": "https://dashboard.gitguardian.com/workspace/1/incidents/xxx",
                "share_url": None,
            },
        }
