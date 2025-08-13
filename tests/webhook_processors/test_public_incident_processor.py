import pytest
from typing import Any
from integration import ObjectKind
from unittest.mock import AsyncMock, patch
from port_ocean.context.ocean import PortOceanContext
from tests.clients.test_client import get_single_mocked_public_secret_incident
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
from port_ocean.core.handlers.port_app_config.models import (
    ResourceConfig,
    Selector,
    PortResourceConfig,
    MappingsConfig,
    EntityMapping,
)
from webhook_processors.public_incident_webhook_processor import (
    PublicSecretIncidentWebhookProcessor,
)


@pytest.fixture
def public_incident_webhook_processor(
    mock_event: WebhookEvent,
) -> PublicSecretIncidentWebhookProcessor:
    return PublicSecretIncidentWebhookProcessor(mock_event)


@pytest.fixture
def public_incident_resource_config() -> ResourceConfig:
    # Create a mock selector with the required generate_request_params method
    class MockPublicSecretIncidentSelector(Selector):
        def generate_request_params(self) -> dict[str, Any]:
            return {}

    return ResourceConfig(
        kind="internal_secret_incident",
        selector=MockPublicSecretIncidentSelector(query="test"),
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

    @pytest.mark.asyncio
    async def test_handle_event_incident_shared_publicly(
        self,
        public_incident_webhook_processor: PublicSecretIncidentWebhookProcessor,
        public_incident_resource_config: ResourceConfig,
    ) -> None:
        payload = self._get_mocked_incident_shared_publicly_payload()
        await self._test_handle_event(
            public_incident_webhook_processor,
            public_incident_resource_config,
            payload,
            "incident_shared_publicly",
        )

    @pytest.mark.asyncio
    async def test_handle_event_incident_unshared_publicly(
        self,
        public_incident_webhook_processor: PublicSecretIncidentWebhookProcessor,
        public_incident_resource_config: ResourceConfig,
    ) -> None:
        payload = self._get_mocked_incident_unshared_publicly_payload()
        await self._test_handle_event(
            public_incident_webhook_processor,
            public_incident_resource_config,
            payload,
            "incident_unshared_publicly",
        )

    async def _test_handle_event(
        self,
        public_incident_webhook_processor,
        public_incident_resource_config,
        payload: dict[str, Any],
        webhook_event_type: str,
    ):
        with patch(
            "webhook_processors.public_incident_webhook_processor.init_gitguardian_client"
        ) as mock_create_client:
            mock_client = AsyncMock()
            mock_http_response = get_single_mocked_public_secret_incident(
                3827964, "aws_iam", "AWS Keys"
            )
            mock_client.get_single_public_secret_incidents.return_value = (
                mock_http_response
            )
            mock_create_client.return_value = mock_client

            if webhook_event_type == "incident_unshared_publicly":
                expected_result = WebhookEventRawResults(
                    updated_raw_results=[],
                    deleted_raw_results=[mock_http_response],
                )
            else:
                expected_result = WebhookEventRawResults(
                    updated_raw_results=[mock_http_response],
                    deleted_raw_results=[],
                )

            actual_result = await public_incident_webhook_processor.handle_event(
                payload=payload, resource_config=public_incident_resource_config
            )

            assert (
                actual_result.updated_raw_results == expected_result.updated_raw_results
            )
            assert (
                actual_result.deleted_raw_results == expected_result.deleted_raw_results
            )

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

    def _get_mocked_incident_unshared_publicly_payload(self) -> EventPayload:
        return {
            "source": "GitGuardian",
            "timestamp": "2022-06-28T08:49:56.806741Z",
            "action": "incident_unshared_publicly",
            "message": "A user has deactivated the public sharing link for this incident.",
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
                "occurrence_count": 2,
                "status": "triggered",
                "declarative_secret_status": "active",
                "regression": False,
                "assignee_email": None,
                "severity": "unknown",
                "ignored_at": None,
                "ignore_reason": None,
                "resolved_at": None,
                "gitguardian_url": "https://dashboard.gitguardian.com/workspace/1/incidents/xxx",
                "share_url": None,
            },
        }
