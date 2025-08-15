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


class BaseGitGuardianWebhookProcessor(AbstractWebhookProcessor):
    async def should_process_event(self, event: WebhookEvent) -> bool:
        if event._original_request is None:
            return False

        return await self._verify_payload_signature(event)

    async def _verify_payload_signature(self, event: WebhookEvent) -> bool:
        # See https://docs.gitguardian.com/platform/configure-alerting/notifiers-integrations/custom-webhook
        signature = event.headers.get("gitguardian-signature", "")

        if not signature.startswith("sha256="):
            return False

        signature = signature.split("sha256=")[-1]
        webhook_secret = ocean.integration_config.get("webhook_secret")
        timestamp = event.headers.get("timestamp", "")

        if signature and not webhook_secret:
            logger.warning(
                "Signature found but no secret configured for authenticating incoming webhooks, skipping event."
            )
            return False

        # Verify signature if webhook secret configured
        body = await event._original_request.body()
        computed_signature = hmac.new(
            bytes(timestamp + webhook_secret, "utf-8"),
            body,
            hashlib.sha256,
        ).hexdigest()

        return hmac.compare_digest(signature, computed_signature)

    async def authenticate(
        self, payload: EventPayload, headers: dict[str, Any]
    ) -> bool:
        # Only basic checks are done here. The payload signature verification is done in should_process_event.
        # See https://ocean.port.io/developing-an-integration/implementing-webhooks/
        webhook_secret_configured = (
            ocean.integration_config.get("webhook_secret") is not None
        )
        has_required_headers = (
            "gitguardian-signature" in headers and "timestamp" in headers
        )
        return webhook_secret_configured and has_required_headers

    def _empty_response(log_message: str) -> WebhookEventRawResults:
        logger.warning(log_message)
        return WebhookEventRawResults(
            updated_raw_results=[],
            deleted_raw_results=[],
        )
