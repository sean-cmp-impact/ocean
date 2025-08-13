import hmac
import json
import time
import pytest
import hashlib
from typing import Any
from integration import ObjectKind
from abc import ABC, abstractmethod
from unittest.mock import AsyncMock, MagicMock
from port_ocean.context.ocean import PortOceanContext
from port_ocean.core.handlers.webhook.webhook_event import WebhookEvent
from webhook_processors.base_webhook_processor import BaseGitGuardianWebhookProcessor
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
def base_processor(
    mock_event: WebhookEvent,
) -> BaseGitGuardianWebhookProcessor:
    return BaseGitGuardianWebhookProcessor(mock_event)


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


class BaseWebhookProcessorTest(ABC):
    """For base functionality only. Polomorphic tests originates from concrete classes"""

    # This line prevents pytest from collecting tests in this base class
    __test__ = False

    async def test_should_process_event_valid_signature_and_timestamp(
        self,
        base_processor: BaseGitGuardianWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        self._set_webhook_secret(mock_context)

        payload = {"action": "incident_triggered"}
        body = json.dumps(payload).encode("utf-8")
        signature = self._get_signature(body, "sha256")
        event = self._init_event(body, signature)

        result = await base_processor.should_process_event(event)
        assert result is True

    async def test_should_process_event_invalid_signature(
        self,
        base_processor: BaseGitGuardianWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        self._set_webhook_secret(mock_context)

        payload = {"action": "incident_triggered"}
        body = json.dumps(payload).encode("utf-8")
        signature = "sha256=invalidsignature"
        event = self._init_event(body, signature)

        result = await base_processor.should_process_event(event)
        assert result is False

    async def test_should_process_event_with_unsupported_hash(
        self,
        base_processor: BaseGitGuardianWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        self._set_webhook_secret(mock_context)

        payload = {"action": "incident_triggered"}
        body = json.dumps(payload).encode("utf-8")
        signature = self._get_signature(body, "md5")
        event = self._init_event(body, signature)

        result = await base_processor.should_process_event(event)
        assert result is False

    async def test_authenticate_with_expected_config_and_headers(
        self,
        base_processor: BaseGitGuardianWebhookProcessor,
        mock_context: PortOceanContext,
    ) -> None:
        self._set_webhook_secret(mock_context)
        payload = {"action": "incident_triggered"}
        body = json.dumps(payload).encode("utf-8")
        signature = self._get_signature(body, "sha256")
        headers = {"gitguardian-signature": signature, "timestamp": TIMESTAMP}

        assert await base_processor.authenticate(payload, headers) is True

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
        payload = {"action": "incident_triggered"}
        body = json.dumps(payload).encode("utf-8")
        signature = self._get_signature(body, "sha256")
        headers = {"gitguardian-signature": signature, "timestamp": TIMESTAMP}

        assert await base_processor.authenticate(payload, headers) is False

    @abstractmethod
    async def test_get_matching_kinds(
        self,
        internal_incident_processor: InternalSecretIncidentWebhookProcessor,
    ) -> None:
        pass

    def _get_signature(self, body: bytes, hash_algorithm: str):
        return f"{hash_algorithm}={hmac.new(
            bytes(TIMESTAMP + WEBHOOK_SECRET, "utf-8"), body, hashlib.sha256
        ).hexdigest()}"

    def _init_event(self, body: bytes, signature: str):
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
