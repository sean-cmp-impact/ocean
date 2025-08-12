from typing import Any
from unittest.mock import AsyncMock, patch
from port_ocean.context.ocean import PortOceanContext
import pytest
from port_ocean.core.handlers.webhook.webhook_event import WebhookEvent
from integration import ObjectKind

# with patch("initialize_client.init_gitguardian_client"):
from webhook_processors.internal_incident_webhook_processor import (
    InternalSecretIncidentWebhookProcessor,
)
from webhook_processors.public_incident_webhook_processor import (
    PublicSecretIncidentWebhookProcessor,
)


@pytest.fixture
def mock_event() -> WebhookEvent:
    return WebhookEvent(trace_id="test", payload={}, headers={})


@pytest.fixture
def internal_incident_processor(
    mock_event: WebhookEvent,
) -> InternalSecretIncidentWebhookProcessor:
    return InternalSecretIncidentWebhookProcessor(mock_event)


@pytest.fixture
def public_incident_webhook_processor(
    mock_event: WebhookEvent,
) -> PublicSecretIncidentWebhookProcessor:
    return PublicSecretIncidentWebhookProcessor(mock_event)


@pytest.fixture
def resource_config() -> Any:
    return {"kind": ObjectKind.INTERNAL_SECRET_INCIDENT}


@pytest.fixture
def mock_context(monkeypatch: Any) -> PortOceanContext:
    mock_context = AsyncMock()
    monkeypatch.setattr(PortOceanContext, "app", mock_context)
    return mock_context


@pytest.mark.asyncio
async def test_should_process_event_valid_signature_and_timestamp(
    internal_incident_processor: InternalSecretIncidentWebhookProcessor,
    mock_context: PortOceanContext,
) -> None:
    with patch("webhook_processors.base_webhook_processor.hmac") as mock_hmac:
        mock_hmac_obj = mock_hmac.new.return_value
        mock_hmac_obj.hexdigest.return_value = "1234567890"

        mock_request = AsyncMock()
        mock_request.body.return_value = b'{"event":"project.created"}'

        event = WebhookEvent(
            trace_id="test-trace-id",
            payload={
                "event": "project.created",
            },
            headers={
                "gitguardian-signature": "sha256=1234567890",
                "timestamp": "0",
            },
        )
        event._original_request = mock_request

        assert await internal_incident_processor.should_process_event(event) is True

        mock_hmac_obj.hexdigest.return_value = "1"
        assert await internal_incident_processor.should_process_event(event) is False
