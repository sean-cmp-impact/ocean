import hashlib
import hmac
from typing import Any
from loguru import logger
from port_ocean.context.ocean import ocean
from port_ocean.core.handlers.webhook.abstract_webhook_processor import (
    AbstractWebhookProcessor,
)
from port_ocean.core.handlers.webhook.webhook_event import (
    EventPayload,
    WebhookEvent,
    WebhookEventRawResults,
)
from webhook_processors.webhook_events import WEBHOOK_EVENTS


class BaseGitGuardianWebhookProcessor(AbstractWebhookProcessor):
    async def should_process_event(self, event: WebhookEvent) -> bool:
        if event._original_request is None:
            return False

        return event.payload.get("action") in WEBHOOK_EVENTS

    async def _verify_payload_signature(
        self, payload: str, headers: dict[str, Any]
    ) -> bool:
        # See https://docs.gitguardian.com/platform/configure-alerting/notifiers-integrations/custom-webhook
        signature = headers.get("gitguardian-signature", "")

        if not signature.startswith("sha256="):
            return False

        signature = signature.split("sha256=")[-1]
        webhook_secret = ocean.integration_config.get("gitguardian_webhook_secret")
        timestamp = headers.get("timestamp", "")

        if webhook_secret is None:
            logger.warning(
                "No webhook secret configured for authenticating incoming webhooks, skipping event."
            )
            return False

        computed_signature = hmac.new(
            key=bytes(timestamp + webhook_secret, "utf-8"),
            msg=bytes(payload, "utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        return hmac.compare_digest(signature, computed_signature)

    async def authenticate(
        self, payload: EventPayload, headers: dict[str, Any]
    ) -> bool:
        if not payload:
            return False

        await self._verify_payload_signature(str(payload), headers)

    def _empty_response(self, log_message: str) -> WebhookEventRawResults:
        logger.warning(log_message)
        return WebhookEventRawResults(
            updated_raw_results=[],
            deleted_raw_results=[],
        )
