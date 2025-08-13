from loguru import logger
from port_ocean.core.handlers.port_app_config.models import ResourceConfig
from port_ocean.core.handlers.webhook.webhook_event import (
    EventPayload,
    WebhookEvent,
    WebhookEventRawResults,
)

from initialize_client import init_gitguardian_client
from integration import ObjectKind
from webhook_processors.base_webhook_processor import BaseGitGuardianWebhookProcessor


class InternalSecretIncidentWebhookProcessor(BaseGitGuardianWebhookProcessor):
    async def get_matching_kinds(self, event: WebhookEvent) -> list[str]:
        return [ObjectKind.INTERNAL_SECRET_INCIDENT]

    async def handle_event(
        self, payload: EventPayload, resource_config: ResourceConfig
    ) -> WebhookEventRawResults:
        incident_id = payload.get("incident", {}).get("id")

        if incident_id is None:
            return self._empty_response(
                "Failed to retrieve an incident ID from the payload."
            )

        logger.debug(f"Fetching incident with ID: {incident_id}")
        client = await init_gitguardian_client()
        incident_data = await client.get_single_internal_secret_incidents(incident_id)

        if incident_data is None:
            return self._empty_response(
                f"Failed to retrieve an incident with ID: {incident_id}"
            )

        logger.info(f"Processing incident: {incident_id}")
        return WebhookEventRawResults(
            updated_raw_results=[incident_data],
            deleted_raw_results=[],
        )

    async def validate_payload(self, payload: EventPayload) -> bool:
        return payload.get("action", "").startswith("incident_")
