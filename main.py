from typing import cast
from loguru import logger
from port_ocean.context.ocean import ocean
from gitguardian.overrides import (
    GitGuardianAuditLogConfig,
    GitGuardianCustomTagConfig,
    GitGuardianDeveloperConfig,
    GitGuardianInternalSecretIncidentConfig,
    GitGuardianPublicSecretIncidentConfig,
    GitGuardianSecretDetectorConfig,
    GitGuardianSourceConfig,
    GitGuardianTeamConfig,
    GitGuardianTeamMemberConfig,
    GitGuardianWorkspaceMemberConfig,
)
from initialize_client import init_gitguardian_client
from port_ocean.context.event import event
from port_ocean.core.ocean_types import ASYNC_GENERATOR_RESYNC_TYPE
from integration import ObjectKind
from utils import (
    produce_audit_log_query_params,
    produce_developer_query_params,
    produce_internal_secret_incidents_query_params,
    produce_public_secret_incidents_query_params,
    produce_secret_detector_query_params,
    produce_source_query_params,
    produce_team_member_query_params,
    produce_team_query_params,
    produce_workspace_member_query_params,
)
from webhook_processors.internal_incident_webhook_processor import (
    InternalSecretIncidentWebhookProcessor,
)
from webhook_processors.public_incident_webhook_processor import (
    PublicSecretIncidentWebhookProcessor,
)


@ocean.on_start()
async def on_start() -> None:
    logger.info("Starting GitGuardian integration")
    if ocean.event_listener_type == "ONCE":
        logger.info("Skipping webhook creation because the event listener is ONCE")
        return


@ocean.on_resync(ObjectKind.SOURCE)
async def on_resync_sources(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client()
    selector = cast(GitGuardianSourceConfig, event.resource_config).selector

    query_params = produce_source_query_params(selector)

    async for sources in gitguardian_client.get_sources(query_params):
        logger.info(f"Received source batch with {len(sources)} sources")
        yield sources


@ocean.on_resync(ObjectKind.SECRET_DETECTOR)
async def on_resync_detectors(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client()
    selector = cast(GitGuardianSecretDetectorConfig, event.resource_config).selector

    query_params = produce_secret_detector_query_params(selector)

    async for detectors in gitguardian_client.get_secret_detectors(query_params):
        logger.info(f"Received secret detector batch with {len(detectors)} detectors")
        yield detectors


@ocean.on_resync(ObjectKind.INTERNAL_SECRET_INCIDENT)
async def on_resync_internal_secret_incidents(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client()
    selector = cast(
        GitGuardianInternalSecretIncidentConfig, event.resource_config
    ).selector

    query_params = produce_internal_secret_incidents_query_params(selector)

    async for internal_incidents in gitguardian_client.get_internal_secret_incidents(
        query_params
    ):
        logger.info(
            f"Received internal secrets incident batch with {len(internal_incidents)} incidents"
        )
        yield internal_incidents


@ocean.on_resync(ObjectKind.PUBLIC_SECRET_INCIDENT)
async def on_resync_public_secret_incidents(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client()
    selector = cast(
        GitGuardianPublicSecretIncidentConfig, event.resource_config
    ).selector

    query_params = produce_public_secret_incidents_query_params(selector)

    async for public_incidents in gitguardian_client.get_public_secret_incidents(
        query_params
    ):
        logger.info(
            f"Received public secrets incident batch with {len(public_incidents)} incidents"
        )
        yield public_incidents


@ocean.on_resync(ObjectKind.TEAM)
async def on_resync_teams(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client()
    selector = cast(GitGuardianTeamConfig, event.resource_config).selector

    query_params = produce_team_query_params(selector)

    async for teams in gitguardian_client.get_teams(query_params):
        logger.info(f"Received teams batch with {len(teams)} incidents")
        yield teams


@ocean.on_resync(ObjectKind.WORKSPACE_MEMBER)
async def on_resync_members(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client()
    selector = cast(GitGuardianWorkspaceMemberConfig, event.resource_config).selector

    query_params = produce_workspace_member_query_params(selector)

    async for members in gitguardian_client.get_workspace_members(query_params):
        logger.info(f"Received workspace members batch with {len(members)} members")
        yield members


@ocean.on_resync(ObjectKind.TEAM_MEMBER)
async def on_resync_members(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client()
    selector = cast(GitGuardianTeamMemberConfig, event.resource_config).selector
    team_id = selector.team_id

    if team_id is None:
        logger.warning("Team ID is not set in the selector, skipping team member sync.")
        return

    query_params = produce_team_member_query_params(selector)

    async for members in gitguardian_client.get_team_membership(team_id, query_params):
        logger.info(f"Received team members batch with {len(members)} members")
        yield members


@ocean.on_resync(ObjectKind.DEVELOPER)
async def on_resync_developers(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client()
    selector = cast(GitGuardianDeveloperConfig, event.resource_config).selector

    query_params = produce_developer_query_params(selector)

    async for developers in gitguardian_client.get_developers(query_params):
        logger.info(f"Received members batch with {len(developers)} developers")
        yield developers


@ocean.on_resync(ObjectKind.AUDIT_LOG)
async def on_resync_audit_log(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client()
    selector = cast(GitGuardianAuditLogConfig, event.resource_config).selector

    query_params = produce_audit_log_query_params(selector)

    async for audit_logs in gitguardian_client.get_audit_logs(query_params):
        logger.info(f"Received audit logs batch with {len(audit_logs)} logs")
        yield audit_logs


@ocean.on_resync(ObjectKind.CUSTOM_TAG)
async def on_resync_custom_tags(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client()
    selector = cast(GitGuardianCustomTagConfig, event.resource_config).selector

    query_params = {"key": selector.key} if getattr(selector, "key", None) else {}

    async for custom_tags in gitguardian_client.get_custom_tags(query_params):
        logger.info(f"Received custom tags batch with {len(custom_tags)} tags")
        yield custom_tags


ocean.add_webhook_processor("/webhook", InternalSecretIncidentWebhookProcessor)
ocean.add_webhook_processor("/webhook", PublicSecretIncidentWebhookProcessor)
