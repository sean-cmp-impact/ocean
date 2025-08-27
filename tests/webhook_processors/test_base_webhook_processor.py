import hmac
import json
import time
from typing import Any
import pytest
import hashlib
from abc import ABC, abstractmethod
from unittest.mock import AsyncMock, MagicMock
from port_ocean.context.ocean import PortOceanContext
from port_ocean.core.handlers.webhook.webhook_event import WebhookEvent
from webhook_processors.base_webhook_processor import BaseGitGuardianWebhookProcessor


WEBHOOK_SECRET = "testsecret"
TIMESTAMP = str(time.time())
DEFAULT_PAYLOAD = {"action": "incident_triggered"}


@pytest.fixture
def base_processor(
    mock_event: WebhookEvent,
) -> BaseGitGuardianWebhookProcessor:
    return BaseGitGuardianWebhookProcessor(mock_event)


@pytest.fixture
def mock_event() -> WebhookEvent:
    return WebhookEvent(trace_id="test", payload={}, headers={})


@pytest.fixture
def mock_context(monkeypatch: Any) -> MagicMock:
    mock_context = MagicMock()
    monkeypatch.setattr(PortOceanContext, "app", mock_context)
    return mock_context


class BaseWebhookProcessorTest(ABC):
    """For base functionality only. Polomorphic tests originate from concrete classes"""

    # This line prevents pytest from collecting tests in this base class
    __test__ = False

    async def test_should_process_event_valid_signature_and_timestamp(
        self,
        base_processor: BaseGitGuardianWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        self._set_webhook_secret(mock_context)

        body = json.dumps(DEFAULT_PAYLOAD).encode("utf-8")
        signature = self._make_signature(body)
        event = self._make_event(body, signature)

        result = await base_processor.should_process_event(event)
        assert result is True

    async def test_should_process_event_invalid_signature(
        self,
        base_processor: BaseGitGuardianWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        self._set_webhook_secret(mock_context)

        body = json.dumps(DEFAULT_PAYLOAD).encode("utf-8")
        signature = "sha256=invalidsignature"
        event = self._make_event(body, signature)

        result = await base_processor.should_process_event(event)
        assert result is False

    async def test_should_process_event_with_unsupported_hash(
        self,
        base_processor: BaseGitGuardianWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        self._set_webhook_secret(mock_context)

        body = json.dumps(DEFAULT_PAYLOAD).encode("utf-8")
        signature = self._make_signature(body, hashlib.md5)
        event = self._make_event(body, signature)

        result = await base_processor.should_process_event(event)
        assert result is False

    async def test_authenticate_with_expected_config_and_headers(
        self,
        base_processor: BaseGitGuardianWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        self._set_webhook_secret(mock_context)
        body = json.dumps(DEFAULT_PAYLOAD).encode("utf-8")
        signature = self._make_signature(body)
        headers = {"gitguardian-signature": signature, "timestamp": TIMESTAMP}

        assert await base_processor.authenticate(DEFAULT_PAYLOAD, headers) is True

    async def test_authenticate_with_expected_config_and_no_headers(
        self,
        base_processor: BaseGitGuardianWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        self._set_webhook_secret(mock_context)
        assert await base_processor.authenticate({}, {}) is False

    async def test_authenticate_with_expected_headers_and_no_config(
        self,
        base_processor: BaseGitGuardianWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        self._unset_webhook_secret(mock_context)
        body = json.dumps(DEFAULT_PAYLOAD).encode("utf-8")
        signature = self._make_signature(body)
        headers = {"gitguardian-signature": signature, "timestamp": TIMESTAMP}

        assert await base_processor.authenticate(DEFAULT_PAYLOAD, headers) is False

    @abstractmethod
    async def test_get_matching_kinds(
        self,
        base_processor: BaseGitGuardianWebhookProcessor,
    ) -> None:
        pass

    def _make_signature(self, body: bytes, hash_algorithm: hashlib = hashlib.sha256):
        return f"{hash_algorithm().name}={hmac.new(
            bytes(TIMESTAMP + WEBHOOK_SECRET, "utf-8"), body, hash_algorithm
        ).hexdigest()}"

    def _make_event(self, body: bytes, signature: str):
        event = MagicMock()
        event._original_request = MagicMock()
        event._original_request.body = AsyncMock(return_value=body)
        event.headers = {"gitguardian-signature": signature, "timestamp": TIMESTAMP}
        return event

    def _set_webhook_secret(self, mock_context: PortOceanContext) -> None:
        self._set_integration_config(mock_context, {"webhook_secret": WEBHOOK_SECRET})

    def _unset_webhook_secret(self, mock_context: PortOceanContext) -> None:
        self._set_integration_config(mock_context, {"webhook_secret": None})

    def _set_integration_config(
        self, mock_context: PortOceanContext, config: dict[str, str]
    ) -> None:
        mock_config = MagicMock()
        mock_config.integration.config = config
        mock_context.config = mock_config
