import httpx
from httpx import URL, Response
from enum import StrEnum
from typing import AsyncGenerator, Optional, Any
from port_ocean.utils import http_async_client
from loguru import logger

PAGE_SIZE = 50


class Endpoints(StrEnum):
    AUDIT_LOGS = "audit_logs"
    CUSTOM_TAGS = "custom_tags"
    DEVELOPERS = "public-perimeter/developers"
    HEALTH = "health"
    INTERNAL_SECRET_INCIDENTS = "incidents/secrets"
    INTERNAL_SECRET_OCCURRENCES = "occurrences/secrets"
    WORKSPACE_MEMBERS = "members"
    PUBLIC_SECRET_INCIDENTS = "public-incidents/secrets"
    SOURCES = "sources"
    SECRET_DETECTORS = "secret_detectors"
    TEAMS = "teams"


class GitGuardianClient:
    def __init__(self, base_url: str, api_key: str, api_version: str):
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
    ) -> Response:
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
            return {"data": response.json(), "links": response.links}
        except (httpx.HTTPStatusError, Exception) as e:
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
                response = await self._send_api_request(
                    endpoint=endpoint,
                    method=method,
                    query_params={**(query_params or {}), "per_page": PAGE_SIZE},
                )

                data = response.get("data", [])
                yield data

                links = response.get("links", [])
                if not links:
                    break

                next_url = links.get("next", {})["url"]
                if next_url:
                    parsed_url = URL(next_url)
                    endpoint = parsed_url.raw_path.decode().replace(
                        f"{self.base_url}/{self.api_version}", ""
                    )
                    query_params = dict(parsed_url.params)
                else:
                    endpoint = ""
                    query_params = {}
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"HTTP error with status code: {e.response.status_code} and response text: {e.response.text}"
                )
                raise

    async def get_audit_logs(
        self, query_params: Optional[dict[str, Any]] = None
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching all audit logs from GitGuardian.")
        async for audit_logs in self._send_paginated_request(
            endpoint=Endpoints.AUDIT_LOGS, query_params=query_params
        ):
            yield audit_logs

    async def get_custom_tags(
        self, query_params: Optional[dict[str, Any]] = None
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching all existing custom tags from GitGuardian.")
        async for custom_tags in self._send_api_request(
            endpoint=Endpoints.CUSTOM_TAGS, query_params=query_params
        ):
            yield custom_tags

    async def get_developers(self) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching developers in the public perimeter from GitGuardian.")
        async for developers in self._send_api_request(endpoint=Endpoints.DEVELOPERS):
            yield developers

    async def get_health(self) -> dict[str, Any]:
        logger.info(f"Checking the status of the API and token.")
        return await self._send_api_request(endpoint=Endpoints.HEALTH)

    async def get_internal_secret_incidents(
        self,
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching secret incidents detected by the GitGuardian dashboard.")
        async for incidents in self._send_paginated_request(
            endpoint=Endpoints.INTERNAL_SECRET_INCIDENTS
        ):
            yield incidents

    async def get_single_internal_secret_incidents(
        self, incident_id: int
    ) -> dict[str, Any]:
        logger.info(
            f"Fetching specific secret incidents detected by the GitGuardian dashboard."
        )
        result = await self._send_api_request(
            endpoint=f"{Endpoints.INTERNAL_SECRET_INCIDENTS}/{incident_id}"
        )
        return result.get("data")

    async def get_internal_secret_occurrences(
        self,
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching occurrences of secrets in the monitored perimeter.")
        async for occurrences in self._send_api_request(
            endpoint=Endpoints.INTERNAL_SECRET_OCCURRENCES
        ):
            yield occurrences

    async def get_workspace_members(self) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching all members of the GitGuardian workspace.")
        async for members in self._send_paginated_request(
            endpoint=Endpoints.WORKSPACE_MEMBERS
        ):
            yield members

    async def get_single_workspace_member(self, member_id: int) -> dict[str, Any]:
        logger.info(f"Fetching specific GitGuardian workspace member.")
        result = await self._send_api_request(
            endpoint=f"{Endpoints.WORKSPACE_MEMBERS}/{member_id}"
        )
        return result.get("data")

    async def get_member_teams(
        self, member_id: int
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching all members of the GitGuardian workspace.")
        async for member_teams in self._send_api_request(
            endpoint=f"{Endpoints.WORKSPACE_MEMBERS}/{member_id}/teams"
        ):
            yield member_teams

    async def get_public_secret_incidents(
        self,
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(
            f"Fetching public secret incidents detected by the GitGuardian dashboard."
        )
        async for public_incidents in self._send_api_request(
            endpoint=Endpoints.PUBLIC_SECRET_INCIDENTS
        ):
            yield public_incidents

    async def get_single_public_secret_incidents(
        self, incident_id: int
    ) -> dict[str, Any]:
        logger.info(
            f"Fetching specific public secret incidents detected by the GitGuardian dashboard."
        )
        result = await self._send_api_request(
            endpoint=f"{Endpoints.PUBLIC_SECRET_INCIDENTS}/{incident_id}"
        )
        return result.get("data")

    async def get_public_secret_occurrences(
        self, incident_id: int
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(
            f"Fetching public secret occurrences detected by the GitGuardian dashboard."
        )
        async for public_occurrences in self._send_api_request(
            endpoint=f"{Endpoints.PUBLIC_SECRET_INCIDENTS}/{incident_id}/occurrences"
        ):
            yield public_occurrences

    async def get_sources(
        self, query_params: Optional[dict[str, Any]] = None
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching all sources known by GitGuardian.")
        async for sources in self._send_paginated_request(
            endpoint=Endpoints.SOURCES, query_params=query_params
        ):
            yield sources

    async def get_single_source(self, source_id: int) -> dict[str, Any]:
        logger.info(f"Fetching a single source known by GitGuardian.")
        result = await self._send_api_request(
            endpoint=f"{Endpoints.SOURCES}/{source_id}"
        )
        return result.get("data")

    async def get_sources_secret_incidents(
        self, source_id: int
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching secret incidents linked to a source.")
        async for source_incidents in self._send_paginated_request(
            endpoint=f"{Endpoints.SOURCES}/{source_id}/incidents/secrets"
        ):
            yield source_incidents

    async def get_secret_detectors(self) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching all secret detectors.")
        async for detectors in self._send_paginated_request(
            endpoint=Endpoints.SECRET_DETECTORS
        ):
            yield detectors

    async def get_teams(self) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching all teams in GitGuardian workspace.")
        async for teams in self._send_paginated_request(endpoint=Endpoints.TEAMS):
            yield teams

    async def get_single_team(self, team_id: int) -> dict[str, Any]:
        logger.info(f"Fetching a single source known by GitGuardian.")
        result = await self._send_api_request(endpoint=f"{Endpoints.TEAMS}/{team_id}")
        return result.get("data")

    async def get_team_secrets(
        self, team_id: int
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching all teams in GitGuardian workspace.")
        async for team_secrets in self._send_paginated_request(
            endpoint=f"{Endpoints.TEAMS}/{team_id}/secret-incidents"
        ):
            yield team_secrets

    async def get_team_membership(
        self, team_id: int
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching all memberships of a team.")
        async for team_memberships in self._send_paginated_request(
            endpoint=f"{Endpoints.TEAMS}/{team_id}/team_memberships"
        ):
            yield team_memberships

    async def get_team_sources(
        self, team_id: int
    ) -> AsyncGenerator[list[dict[str, Any]], None]:
        logger.info(f"Fetching all sources belonging to a team's perimeter.")
        async for team_sources in self._send_paginated_request(
            endpoint=f"{Endpoints.TEAMS}/{team_id}/sources"
        ):
            yield team_sources
