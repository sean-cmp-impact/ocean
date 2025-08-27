from typing import cast
from loguru import logger
from port_ocean.context.ocean import ocean
from gitguardian.overrides import (
    GitGuardianInternalSecretIncidentConfig,
    GitGuardianPublicSecretIncidentConfig,
    GitGuardianSecretDetectorConfig,
    GitGuardianSourceConfig,
    GitGuardianUserConfig,
)
from initialize_client import init_gitguardian_client
from port_ocean.context.event import event
from port_ocean.core.ocean_types import ASYNC_GENERATOR_RESYNC_TYPE
from integration import ObjectKind
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

    async for sources in gitguardian_client.get_sources(
        selector.produce_query_params()
    ):
        logger.info(f"Received source batch with {len(sources)} sources")
        yield sources


@ocean.on_resync(ObjectKind.SECRET_DETECTOR)
async def on_resync_detectors(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client()
    selector = cast(GitGuardianSecretDetectorConfig, event.resource_config).selector

    async for detectors in gitguardian_client.get_secret_detectors(
        selector.produce_query_params()
    ):
        logger.info(f"Received secret detector batch with {len(detectors)} detectors")
        yield detectors


@ocean.on_resync(ObjectKind.INTERNAL_SECRET_INCIDENT)
async def on_resync_internal_secret_incidents(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client()
    selector = cast(
        GitGuardianInternalSecretIncidentConfig, event.resource_config
    ).selector

    async for internal_incidents in gitguardian_client.get_internal_secret_incidents(
        selector.produce_query_params()
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

    async for public_incidents in gitguardian_client.get_public_secret_incidents(
        selector.produce_query_params()
    ):
        logger.info(
            f"Received public secrets incident batch with {len(public_incidents)} incidents"
        )
        yield public_incidents


@ocean.on_resync(ObjectKind.USER)
async def on_resync_members(kind: str) -> ASYNC_GENERATOR_RESYNC_TYPE:
    gitguardian_client = await init_gitguardian_client()
    selector = cast(GitGuardianUserConfig, event.resource_config).selector

    async for members in gitguardian_client.get_users(selector.produce_query_params()):
        logger.info(f"Received users batch with {len(members)} members")
        yield members


ocean.add_webhook_processor("/webhook", InternalSecretIncidentWebhookProcessor)
ocean.add_webhook_processor("/webhook", PublicSecretIncidentWebhookProcessor)
