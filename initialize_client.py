from client import GitGuardianClient
from port_ocean.context.ocean import ocean

def init_gitguardian_client() -> GitGuardianClient:
    return GitGuardianClient(
        ocean.integration_config.get("gitguardian_api_base_url"),
        ocean.integration_config.get("gitguardian_api_token"),
    )