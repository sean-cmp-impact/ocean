from typing import cast
from gitguardian.overrides import GitGuardianWorkspaceMemberConfig
from initialize_client import init_gitguardian_client
from port_ocean.core.handlers.port_app_config.models import ResourceConfig
from port_ocean.core.handlers.webhook.webhook_event import (
    EventPayload,
    WebhookEvent,
    WebhookEventRawResults,
)

from integration import ObjectKind
from webhook_processors.base_webhook_processor import BaseGitGuardianWebhookProcessor


class WorkspaceMemberWebhookProcessor(BaseGitGuardianWebhookProcessor):
    async def get_matching_kinds(self, event: WebhookEvent) -> list[str]:
        return [ObjectKind.WORKSPACE_MEMBER]

    async def handle_event(
        self, payload: EventPayload, resource_config: ResourceConfig
    ) -> WebhookEventRawResults:
        client = init_gitguardian_client()
        config = cast(GitGuardianWorkspaceMemberConfig, resource_config)

        # TODO: Add logic for handling event
