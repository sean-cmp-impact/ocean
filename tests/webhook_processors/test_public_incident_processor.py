import pytest
from integration import ObjectKind
from port_ocean.context.ocean import PortOceanContext
from port_ocean.core.handlers.webhook.webhook_event import WebhookEvent
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
