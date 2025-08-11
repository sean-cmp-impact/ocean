import hashlib
import hmac
from typing import Any
from loguru import logger
from port_ocean.context.ocean import ocean
from port_ocean.core.handlers.webhook.abstract_webhook_processor import (
    AbstractWebhookProcessor,
)
from port_ocean.core.handlers.webhook.webhook_event import EventPayload, WebhookEvent


class BaseGitGuardianWebhookProcessor(AbstractWebhookProcessor):
    async def should_process_event(self, event: WebhookEvent) -> bool:
        if event._original_request is None:
            return False

        # See https://docs.gitguardian.com/platform/configure-alerting/notifiers-integrations/custom-webhook
        webhook_secret = ocean.integration_config.get("webhook_secret")
        signature = event.headers.get("gitguardian-signature", "")
        timestamp = event.headers.get("timestamp", "")

        if signature and not webhook_secret:
            logger.warning(
                "Signature found but no secret configured for authenticating incoming webhooks, skipping event."
            )
            return False

        # Verify signature if webhook secret configured
        body = await event._original_request.body()
        computed_signature = hmac.new(
            (timestamp + webhook_secret).encode("utf-8"),
            body,
            hashlib.sha256,
        ).hexdigest()

        return hmac.compare_digest(signature, computed_signature)

    async def authenticate(
        self, payload: EventPayload, headers: dict[str, Any]
    ) -> bool:
        return True

    async def validate_payload(self, payload: EventPayload) -> bool:
        return payload.get("source", "").lower() == "gitguardian"
