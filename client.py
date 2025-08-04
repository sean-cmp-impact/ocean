import httpx
from httpx import URL
from typing import AsyncGenerator, Optional, Any
from port_ocean.utils import http_async_client
from loguru import logger 

PAGE_SIZE = 50

class Endpoints:
    AUDIT_LOGS = "audit_logs"
    CUSTOM_TAGS = "custom_tags"
    DEVELOPERS = "public-perimeter/developers"
    HEALTH = "health"
    INTERNAL_SECRET_INCIDENTS = "incidents/secrets"
    INTERNAL_SECRET_OCCURRENCES = "occurrences/secrets"
    MEMBERS = "members"
    MEMBE_TEAMS = "members/{member_id}/teams"
    PUBLIC_SECRET_INCIDENTS = "public-incidents/secrets"
    PUBLIC_SECRET_OCCURRENCES = "public-incidents/secrets/{incident_id}/occurrences"
    SOURCES = "sources"
    SOURCE_INCIDENTS = "sources/{source_id}/incidents/secrets"
    SECRET_DETECTORS = "secret_detectors"
    TEAMS = "teams"
    TEAM_MEMBERSHIP = "teams/{team_id}/team_memberships"
    TEAM_SOURCES = "teams/{team_id}/sources"


class GitGuardianClient:
    def __init__(
            self,
            base_url: str,
            api_key: str,
            api_version: str
        ):
        self.base_url = base_url
        self.api_key = api_key
        self.api_version = api_version
        self.http_client = http_async_client
        self.http_client.base_url = base_url.rstrip("/")
        self.http_client.headers.update(self.api_auth_params["headers"])

    @property
    def api_auth_params(self) -> dict[str, Any]:
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
        query_params: Optional[dict[str, Any]] = None,
        json_data: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        logger.debug(
            f"Sending API request to {method} {endpoint} with query params: {query_params}"
        )
        try:
            response = await self.http_client.request(
                method=method,
                url=f"{self.base_url}/{self.api_version}/{endpoint}",
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

    async def _send_paginated_request(
        self,
        endpoint: str,
        method: str = "GET",
        query_params: Optional[dict[str, Any]] = None,
    ) -> AsyncGenerator[list[Any], None]:
        while endpoint:
            try:
                data = await self._send_api_request(
                    endpoint=endpoint,
                    method=method,
                    query_params={**(query_params or {}), "per_page": PAGE_SIZE},
                )

                yield data.get("data", [])

                # Check if there is a "next" URL in the links object
                next_url = data.get("links", {}).get("next", "url")
                if next_url:
                    parsed_url = URL(next_url)
                    endpoint = parsed_url.raw_path.decode().replace(f"{self.base_url}/{self.api_version}", "")
                    query_params = dict(parsed_url.params)
                else:
                    endpoint = ""
                    query_params = {}
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"HTTP error with status code: {e.response.status_code} and response text: {e.response.text}"
                )
                raise    

    async def get_audit_logs(self) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching all audit logs from GitGuardian.")
        async for audit_logs in self._send_api_request(endpoint=Endpoints.AUDIT_LOGS):
            yield audit_logs

    async def get_custom_tags(self) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching all existing custom tags from GitGuardian.")
        async for custom_tags in self._send_api_request(endpoint=Endpoints.CUSTOM_TAGS):
            yield custom_tags

    async def get_developers(self) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching developers in the public perimeter from GitGuardian.")
        async for developers in self._send_api_request(endpoint=Endpoints.DEVELOPERS):
            yield developers

    async def get_health(self) -> dict[str, Any]:        
        logger.info(f"Checking the status of the API and token.")
        return await self._send_api_request(endpoint=Endpoints.HEALTH)
    
    async def get_internal_secret_incidents(self) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching secret incidents detected by the GitGuardian dashboard.")
        async for incidents in self._send_api_request(endpoint=Endpoints.INTERNAL_SECRET_INCIDENTS):
            yield incidents

    async def get_single_internal_secret_incidents(self, incident_id: int) -> dict[str, Any]:   
        logger.info(f"Fetching specific secret incidents detected by the GitGuardian dashboard.")
        return await self._send_api_request(endpoint=f"{Endpoints.INTERNAL_SECRET_INCIDENTS}/{incident_id}")

    async def get_internal_secret_occurrences(self) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching occurrences of secrets in the monitored perimeter.")
        async for occurrences in self._send_api_request(endpoint=Endpoints.INTERNAL_SECRET_OCCURRENCES):
            yield occurrences

    async def get_sources(self) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching all sources known by GitGuardian")
        async for sources in self._send_paginated_request(endpoint=Endpoints.SOURCES):
            yield sources

    