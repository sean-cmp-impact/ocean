import pytest
from integration import ObjectKind
from port_ocean.context.ocean import PortOceanContext
from port_ocean.core.handlers.webhook.webhook_event import WebhookEvent
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
