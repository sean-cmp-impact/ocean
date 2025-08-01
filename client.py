import httpx
from typing import Optional
from port_ocean.utils import http_async_client
from loguru import logger 

# Use it in your client class
class GitGuardianClient:
    def __init__(
            self,
            base_url: str,
            api_key: str
        ):
        self.base_url = base_url
        self.api_key = api_key
        self.http_client = http_async_client
        self.http_client.base_url = base_url.rstrip("/")
        self.http_client.headers.update(self.api_auth_params["headers"])

    @property
    def api_auth_params(self) -> dict[str, any]:
        return {
            "headers": {
                "Authorization": f"Token {self.api_key}",
                "Content-Type": "application/json", 
            }
        }
    
    async def _send_api_request(
        self,
        endpoint: str,
        method: str = "GET",
        query_params: Optional[dict[str, any]] = None,
        json_data: Optional[dict[str, any]] = None,
    ) -> dict[str, any]:
        logger.debug(
            f"Sending API request to {method} {endpoint} with query params: {query_params}"
        )
        try:
            response = await self.http_client.request(
                method=method,
                url=f"{self.base_url}/v1/{endpoint}",
                params=query_params,
                json=json_data,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP error with status code: {e.response.status_code} and response text: {e.response.text}"
            )
            if e.response.status_code == 404:
                logger.warning(
                    f"Resource not found for endpoint {endpoint} with query params {query_params}: {e.response.text}"
                )
                return {}
            raise

    async def get_sources(self) -> list[any]:
        logger.info(f"Fetching all sources known by GitGuardian")
        response = await self._send_api_request(
            endpoint="sources"
        )
        return response.get("sources", [])