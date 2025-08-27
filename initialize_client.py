from gitguardian.client import GitGuardianClient
from port_ocean.context.ocean import ocean

async def init_gitguardian_client() -> GitGuardianClient:
    return GitGuardianClient(
        ocean.integration_config.get("gitguardian_api_base_url"),
        ocean.integration_config.get("gitguardian_api_token"),
        ocean.integration_config.get("gitguardian_api_version")
    )