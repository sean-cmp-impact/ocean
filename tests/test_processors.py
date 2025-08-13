import hmac
import json
import time
import pytest
import hashlib
from typing import Any
from integration import ObjectKind
from unittest.mock import AsyncMock, MagicMock
from port_ocean.context.ocean import PortOceanContext
from port_ocean.core.handlers.webhook.webhook_event import WebhookEvent
from webhook_processors.internal_incident_webhook_processor import (
    InternalSecretIncidentWebhookProcessor,
)
from webhook_processors.public_incident_webhook_processor import (
    PublicSecretIncidentWebhookProcessor,
)


WEBHOOK_SECRET = "testsecret"
TIMESTAMP = str(time.time())


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
def mock_context(monkeypatch: Any) -> MagicMock:
    mock_context = MagicMock()
    monkeypatch.setattr(PortOceanContext, "app", mock_context)
    return mock_context


@pytest.mark.asyncio
async def test_should_process_event_valid_signature_and_timestamp(
    internal_incident_processor: InternalSecretIncidentWebhookProcessor,
    mock_context: PortOceanContext,
) -> None:
    set_integration_config(mock_context)

    payload = {"action": "incident_triggered"}
    body = json.dumps(payload).encode("utf-8")
    signature = build_signature(body, "sha256")
    event = init_event(body, signature)

    result = await internal_incident_processor.should_process_event(event)
    assert result is True


@pytest.mark.asyncio
async def test_should_process_event_invalid_signature(
    internal_incident_processor: InternalSecretIncidentWebhookProcessor,
    mock_context: PortOceanContext,
) -> None:
    set_integration_config(mock_context)

    payload = {"action": "incident_triggered"}
    body = json.dumps(payload).encode("utf-8")
    signature = "sha256=invalidsignature"
    event = init_event(body, signature)

    result = await internal_incident_processor.should_process_event(event)
    assert result is False


@pytest.mark.asyncio
async def test_should_process_event_with_unsupported_hash(
    internal_incident_processor: InternalSecretIncidentWebhookProcessor,
    mock_context: PortOceanContext,
) -> None:
    set_integration_config(mock_context)

    payload = {"action": "incident_triggered"}
    body = json.dumps(payload).encode("utf-8")
    signature = build_signature(body, "md5")
    event = init_event(body, signature)

    result = await internal_incident_processor.should_process_event(event)
    assert result is False


def build_signature(body, hash_algorithm):
    return f"{hash_algorithm}={hmac.new(
        bytes(TIMESTAMP + WEBHOOK_SECRET, "utf-8"), body, hashlib.sha256
    ).hexdigest()}"


def init_event(body, signature):
    event = MagicMock()
    event._original_request = MagicMock()
    event._original_request.body = AsyncMock(return_value=body)
    event.headers = {"gitguardian-signature": signature, "timestamp": TIMESTAMP}
    return event


def set_integration_config(mock_context) -> None:
    mock_config = MagicMock()
    mock_config.integration.config = {"webhook_secret": WEBHOOK_SECRET}
    mock_context.config = mock_config
