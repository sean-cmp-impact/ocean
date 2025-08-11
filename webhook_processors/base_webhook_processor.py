from typing import Any
from port_ocean.core.handlers.webhook.abstract_webhook_processor import (
    AbstractWebhookProcessor,
)
from port_ocean.core.handlers.webhook.webhook_event import (
    EventPayload,
    WebhookEvent,
)


class BaseGitGuardianWebhookProcessor(AbstractWebhookProcessor):
    async def should_process_event(self, event: WebhookEvent) -> bool:
        return True  # TODO: Improve implementation

    async def authenticate(
        self, payload: EventPayload, headers: dict[str, Any]
    ) -> bool:
        return True  # TODO: Improve this, don't just pass Authentication

    async def validate_payload(self, payload: EventPayload) -> bool:
        return True  # TODO: Improve validation, example: "project" in payload
