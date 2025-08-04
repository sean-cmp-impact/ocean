from typing import Any, cast
from loguru import logger
from port_ocean.context.ocean import ocean
from gitguardian.overrides import (
     GitGuardianAuditLogConfig,
     GitGuardianCustomTagConfig,
     GitGuardianDeveloperConfig,
     GitGuardianMemberConfig,
     GitGuardianSourceConfig,
     GitGuardianSecretDetectorConfig,
     GitGuardianTeamConfig,
     InternalSecretIncidentConfig,
     PublicSecretIncidentConfig 
)
from initialize_client import init_gitguardian_client
from port_ocean.context.event import event
from port_ocean.core.ocean_types import ASYNC_GENERATOR_RESYNC_TYPE
from integration import ObjectKind


# Optional
# Listen to the start event of the integration. Called once when the integration starts.
@ocean.on_start()
async def on_start() -> None:
    logger.info("Starting GitGuardian integration")
    if ocean.event_listener_type == "ONCE":
        logger.info("Skipping webhook creation because the event listener is ONCE")
        return

@ocean.on_resync(ObjectKind.SOURCE)
async def on_resync_sources(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client() 

    # selector = cast(GitGuardianSourceConfig, event.resource_config).selector
    params = {}

    async for sources in gitguardian_client.get_sources(params):
        logger.info(f"Received source batch with {len(sources)} sources")
        yield sources

@ocean.on_resync(ObjectKind.SECRET_DETECTOR)
async def on_resync_detectors(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client() 

    # selector = cast(GitGuardianSecretDetectorConfig, event.resource_config).selector
    params = {}

    async for detectors in gitguardian_client.get_secret_detectors(params):
        logger.info(f"Received secret detector batch with {len(detectors)} detectors")
        yield detectors

@ocean.on_resync(ObjectKind.INTERNAL_SECRET_INCIDENT)
async def on_resync_internal_secret_incidents(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client() 

    # selector = cast(InternalSecretIncidentConfig, event.resource_config).selector
    params = {}

    async for internal_incidents in gitguardian_client.get_internal_secret_incidents(params):
        logger.info(f"Received internal secrets incident batch with {len(internal_incidents)} incidents")
        yield internal_incidents

@ocean.on_resync(ObjectKind.PUBLIC_SECRET_INCIDENT)
async def on_resync_public_secret_incidents(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client() 

    # selector = cast(PublicSecretIncidentConfig, event.resource_config).selector
    params = {}

    async for public_incidents in gitguardian_client.get_public_secret_incidents(params):
        logger.info(f"Received public secrets incident batch with {len(public_incidents)} incidents")
        yield public_incidents

@ocean.on_resync(ObjectKind.TEAM)
async def on_resync_teams(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client() 

    # selector = cast(GitGuardianTeamConfig, event.resource_config).selector
    params = {}

    async for teams in gitguardian_client.get_teams(params):
        logger.info(f"Received teams batch with {len(teams)} incidents")
        yield teams

@ocean.on_resync(ObjectKind.MEMBER)
async def on_resync_members(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client() 

    # selector = cast(GitGuardianMemberConfig, event.resource_config).selector
    params = {}

    async for members in gitguardian_client.get_members(params):
        logger.info(f"Received members batch with {len(members)} members")
        yield members

@ocean.on_resync(ObjectKind.DEVELOPER)
async def on_resync_developers(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client() 

    # selector = cast(GitGuardianDeveloperConfig, event.resource_config).selector
    params = {}

    async for developers in gitguardian_client.get_developers(params):
        logger.info(f"Received members batch with {len(developers)} developers")
        yield developers

@ocean.on_resync(ObjectKind.AUDIT_LOG)
async def on_resync_audit_log(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client() 

    # selector = cast(GitGuardianAuditLogConfig, event.resource_config).selector
    params = {}

    async for audit_logs in gitguardian_client.get_audit_logs(params):
        logger.info(f"Received audit logs batch with {len(audit_logs)} logs")
        yield audit_logs

@ocean.on_resync(ObjectKind.CUSTOM_TAG)
async def on_resync_custom_tags(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client() 

    # selector = cast(GitGuardianCustomTagConfig, event.resource_config).selector
    params = {}

    async for custom_tags in gitguardian_client.get_audit_logs(params):
        logger.info(f"Received custom tags batch with {len(custom_tags)} tags")
        yield custom_tags



