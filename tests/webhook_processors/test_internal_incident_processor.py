from typing import Any
from unittest.mock import AsyncMock, patch
import pytest
from gitguardian.client import GitGuardianClient
from integration import ObjectKind
from tests.clients.test_client import get_single_mocked_internal_secret_incident
from port_ocean.context.ocean import PortOceanContext
from port_ocean.core.handlers.port_app_config.models import (
    ResourceConfig,
    Selector,
    PortResourceConfig,
    MappingsConfig,
    EntityMapping,
)
from port_ocean.core.handlers.webhook.webhook_event import (
    WebhookEvent,
    EventPayload,
    WebhookEventRawResults,
)
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


@pytest.fixture
def internal_incident_resource_config() -> ResourceConfig:
    # Create a mock selector with the required generate_request_params method
    class MockInternalSecretIncidentSelector(Selector):
        def generate_request_params(self) -> dict[str, Any]:
            return {}

    return ResourceConfig(
        kind="internal_secret_incident",
        selector=MockInternalSecretIncidentSelector(query="test"),
        port=PortResourceConfig(
            entity=MappingsConfig(
                mappings=EntityMapping(
                    identifier=".id",
                    title=".name",
                    blueprint='"gitguardianSecretIncident"',
                    properties={},
                    relations={},
                )
            )
        ),
    )


@pytest.fixture
def mock_gitguardian_client() -> GitGuardianClient:
    """Fixture to initialize GitGuardianClient with mock parameters."""
    return GitGuardianClient(
        base_url="https://mockapi.gitguardian.com",
        api_key="test_api_key",
        api_version="v1",
    )


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
    @pytest.mark.parametrize(
        "payload,expected",
        [
            ({"action": "incident_assigned"}, True),
            ({"action": "some_other_action"}, False),
            ({}, False),
        ],
    )
    async def test_validate_payload_variants(
        self,
        internal_incident_processor: InternalSecretIncidentWebhookProcessor,
        payload: dict,
        expected: bool,
    ) -> None:
        """Test payload validation for various action types."""
        result = await internal_incident_processor.validate_payload(payload=payload)
        assert result is expected

    @pytest.mark.asyncio
    async def test_handle_event(
        self,
        internal_incident_processor: InternalSecretIncidentWebhookProcessor,
        internal_incident_resource_config: ResourceConfig,
    ) -> None:
        with patch(
            "webhook_processors.internal_incident_webhook_processor.init_gitguardian_client"
        ) as mock_create_client:
            mock_client = AsyncMock()
            mock_http_response = get_single_mocked_internal_secret_incident(
                31450, "generic_password", "Generic Password"
            )
            mock_client.get_single_internal_secret_incidents.return_value = (
                mock_http_response
            )
            mock_create_client.return_value = mock_client

            payload = self._get_mocked_assign_event_payload()
            expected_result = WebhookEventRawResults(
                updated_raw_results=[mock_http_response],
                deleted_raw_results=[],
            )

            actual_result = await internal_incident_processor.handle_event(
                payload=payload, resource_config=internal_incident_resource_config
            )

            assert (
                actual_result.updated_raw_results == expected_result.updated_raw_results
            )
            assert (
                actual_result.deleted_raw_results == expected_result.deleted_raw_results
            )

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
