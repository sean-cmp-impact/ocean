from loguru import logger
from initialize_client import init_gitguardian_client
from port_ocean.core.handlers.port_app_config.models import ResourceConfig
from port_ocean.core.handlers.webhook.webhook_event import (
    EventPayload,
    WebhookEvent,
    WebhookEventRawResults,
)

from integration import ObjectKind
from webhook_processors.base_webhook_processor import BaseGitGuardianWebhookProcessor


class PublicSecretIncidentWebhookProcessor(BaseGitGuardianWebhookProcessor):
    async def get_matching_kinds(self, event: WebhookEvent) -> list[str]:
        return [ObjectKind.PUBLIC_SECRET_INCIDENT]

    async def handle_event(
        self, payload: EventPayload, resource_config: ResourceConfig
    ) -> WebhookEventRawResults:
        webhook_event_type = payload.get("payload", {}).get("action")

        if not webhook_event_type.endswith("_publicly"):
            return self._empty_response(
                f"Attempted to handle incorrect webhook event type: {webhook_event_type}"
            )

        incident_id = payload.get("payload", {}).get("incident", {}).get("id")

        if incident_id is None:
            return self._empty_response(
                "Failed to retrieve an incident ID from the payload."
            )

        logger.debug(f"Fetching public incident with ID: {incident_id}")
        client = await init_gitguardian_client()
        incident_data = await client.get_single_public_secret_incidents(incident_id)

        if incident_data is None:
            return self._empty_response(
                f"Failed to retrieve a public incident with ID: {incident_id}"
            )

        data_to_update = []
        data_to_delete = []
        logger.info(f"Processing public incident: {incident_id}")

        if webhook_event_type == "incident_unshared_publicly":
            data_to_delete.extend([incident_data])
        else:
            data_to_update.extend([incident_data])

        return WebhookEventRawResults(
            updated_raw_results=data_to_update,
            deleted_raw_results=data_to_delete,
        )

    async def validate_payload(self, payload: EventPayload) -> bool:
        return payload.get("payload", {}).get("action", "").endswith("_publicly")
