import pytest
from integration import ObjectKind
from port_ocean.context.ocean import PortOceanContext
from port_ocean.core.handlers.webhook.webhook_event import WebhookEvent, EventPayload
from tests.webhook_processors.test_base_webhook_processor import (
    BaseWebhookProcessorTest,
    mock_event,
    mock_context,
)
from webhook_processors.public_incident_webhook_processor import (
    PublicSecretIncidentWebhookProcessor,
)


@pytest.fixture
def public_incident_webhook_processor(
    mock_event: WebhookEvent,
) -> PublicSecretIncidentWebhookProcessor:
    return PublicSecretIncidentWebhookProcessor(mock_event)


class TestPublicSecretIncidentWebhookProcessor(BaseWebhookProcessorTest):
    __test__ = True

    @pytest.mark.asyncio
    async def test_should_process_event_valid_signature_and_timestamp(
        self,
        public_incident_webhook_processor: PublicSecretIncidentWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        await super().test_should_process_event_valid_signature_and_timestamp(
            public_incident_webhook_processor, mock_context
        )

    @pytest.mark.asyncio
    async def test_should_process_event_invalid_signature(
        self,
        public_incident_webhook_processor: PublicSecretIncidentWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        await super().test_should_process_event_invalid_signature(
            public_incident_webhook_processor, mock_context
        )

    @pytest.mark.asyncio
    async def test_should_process_event_with_unsupported_hash(
        self,
        public_incident_webhook_processor: PublicSecretIncidentWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        await super().test_should_process_event_with_unsupported_hash(
            public_incident_webhook_processor, mock_context
        )

    @pytest.mark.asyncio
    async def test_authenticate_with_expected_config_and_headers(
        self,
        public_incident_webhook_processor: PublicSecretIncidentWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        await super().test_authenticate_with_expected_config_and_headers(
            public_incident_webhook_processor, mock_context
        )

    @pytest.mark.asyncio
    async def test_authenticate_with_expected_config_and_no_headers(
        self,
        public_incident_webhook_processor: PublicSecretIncidentWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        await super().test_authenticate_with_expected_config_and_no_headers(
            public_incident_webhook_processor, mock_context
        )

    @pytest.mark.asyncio
    async def test_authenticate_with_expected_headers_and_no_config(
        self,
        public_incident_webhook_processor: PublicSecretIncidentWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        await super().test_authenticate_with_expected_headers_and_no_config(
            public_incident_webhook_processor, mock_context
        )

    @pytest.mark.asyncio
    async def test_get_matching_kinds(
        self,
        public_incident_webhook_processor: PublicSecretIncidentWebhookProcessor,
    ) -> None:
        event = WebhookEvent(trace_id="test-trace-id", payload={}, headers={})
        result = await public_incident_webhook_processor.get_matching_kinds(event)

        assert result == [ObjectKind.PUBLIC_SECRET_INCIDENT]

    @pytest.mark.asyncio
    async def test_validate_payload_with_publicly_action(
        self,
        public_incident_webhook_processor: PublicSecretIncidentWebhookProcessor,
    ) -> None:
        payload = self._get_mocked_incident_shared_publicly_payload()
        result = await public_incident_webhook_processor.validate_payload(
            payload=payload
        )

        assert result is True

    @pytest.mark.asyncio
    async def test_validate_payload_with_no_publicly_action(
        self,
        public_incident_webhook_processor: PublicSecretIncidentWebhookProcessor,
    ) -> None:
        payload = {"action": "some_other_action"}
        result = await public_incident_webhook_processor.validate_payload(
            payload=payload
        )

        assert result is False

    def _get_mocked_incident_shared_publicly_payload(self) -> EventPayload:
        return {
            "source": "GitGuardian",
            "timestamp": "2022-06-28T08:48:49.290758Z",
            "action": "incident_shared_publicly",
            "message": "A user has generated a public sharing link for this incident.",
            "target_user": "John Doe john.doe@gitguardian.com",
            "target_team": "My team",
            "custom_webhook_name": "My custom webhook name",
            "incident": {
                "id": 3827964,
                "date": "2022-06-23T14:34:11Z",
                "detector": {
                    "name": "aws_iam",
                    "display_name": "AWS Keys",
                    "nature": "specific",
                    "family": "credentials",
                    "detector_group_name": "aws_iam",
                    "detector_group_display_name": "AWS Keys",
                },
                "secret_hash": "xxx",
                "hmsl_hash": "xxx",
                "secret_revoked": False,
                "validity": "invalid",
                "occurrence_count": 1,
                "status": "triggered",
                "declarative_secret_status": "active",
                "regression": False,
                "assignee_email": None,
                "severity": "unknown",
                "ignored_at": None,
                "ignore_reason": None,
                "resolved_at": None,
                "gitguardian_url": "https://dashboard.gitguardian.com/workspace/1/incidents/xx",
                "share_url": "https://dashboard.gitguardian.com/share/incidents/xxx",
            },
        }
