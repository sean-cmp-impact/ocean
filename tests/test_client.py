from typing import Any
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from port_ocean.context.ocean import initialize_port_ocean_context
from port_ocean.exceptions.context import PortOceanContextAlreadyInitializedError
from gitguardian.client import PAGE_SIZE, Endpoints, GitGuardianClient
from httpx import HTTPStatusError, Request, Response


@pytest.fixture(autouse=True)
def mock_ocean_context() -> None:
    """Fixture to mock the Ocean context initialization."""
    try:
        mock_ocean_app = MagicMock()
        mock_ocean_app.config = MagicMock()
        mock_ocean_app.config.oauth_access_token_file_path = None
        mock_ocean_app.config.integration.config = {
            "gitguardian_api_base_url": "https://mockapi.gitguardian.com",
            "gitguardian_api_token": "test_api_key",
            "gitguardian_api_version": "v1"
        }
        mock_ocean_app.integration_router = MagicMock()
        mock_ocean_app.port_client = MagicMock()
        mock_ocean_app.cache_provider = AsyncMock()
        mock_ocean_app.load_external_oauth_access_token = MagicMock(return_value=None)
        mock_ocean_app.cache_provider.get.return_value = None
        initialize_port_ocean_context(mock_ocean_app)
    except PortOceanContextAlreadyInitializedError:
        pass

@pytest.fixture
def mock_gitguardian_client() -> GitGuardianClient:
    """Fixture to initialize GitGuardianClient with mock parameters."""
    return GitGuardianClient(
        base_url="https://mockapi.gitguardian.com",
        api_key="test_api_key",
        api_version="v1",
    )

@pytest.mark.asyncio
async def test_client_initialization(mock_gitguardian_client: GitGuardianClient) -> None:
    """Test the correct initialization of GitGuardianClient."""
    assert mock_gitguardian_client.base_url == "https://mockapi.gitguardian.com"
    assert mock_gitguardian_client.api_key == "test_api_key"
    assert mock_gitguardian_client.api_version == "v1"

@pytest.mark.asyncio
async def test_send_api_request_success(mock_gitguardian_client: GitGuardianClient) -> None:
    """Test successful API requests."""
    with patch.object(
        mock_gitguardian_client.http_client, "request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = Response(
            200, request=Request("GET", "/some_endpoint"), json={"key": "value"}
        )
        response = await mock_gitguardian_client._send_api_request("GET", "/some_endpoint")
        assert response["data"]["key"] == "value"

@pytest.mark.asyncio
async def test_send_api_request_failure(mock_gitguardian_client: GitGuardianClient) -> None:
    """Test API request raising exceptions."""
    with patch.object(
        mock_gitguardian_client.http_client, "request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = Response(
            500, request=Request("GET", "/some_endpoint")
        )        
        with pytest.raises(HTTPStatusError):
            await mock_gitguardian_client._send_api_request("GET", "/some_endpoint")

@pytest.mark.asyncio
async def test_get_single_source(mock_gitguardian_client: GitGuardianClient) -> None:
    """Test get_single_source method"""
    source_id = 123456789
    source_data: dict[str, Any] = get_single_mocked_source(source_id, "test_repo")

    with patch.object(
        mock_gitguardian_client, "_send_api_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = source_data
        result = await mock_gitguardian_client.get_single_source(source_id)

        mock_request.assert_called_once_with(endpoint=f"{Endpoints.SOURCES}/{source_id}")
        assert result == source_data

@pytest.mark.asyncio
async def test_get_sources(mock_gitguardian_client: GitGuardianClient) -> None:
    """Test get_sources method"""
    cursor = "cD0yMDM5NjE4MQ=="
    next_endpoint = f"v1/{Endpoints.SOURCES}?cursor={cursor}&per_page=50";
    sources_response: dict[str, list[dict[str, Any]]] = {
        "data": [f"{get_single_mocked_source(1234, "test_repo")}", f"{get_single_mocked_source(5678, "mock_repo")}"],
        "links": {
            "next": {
                "url": f"https://mockapi.gitguardian.com/{next_endpoint}", "rel": "next"
            }
        }
    }
    empty_response: dict[str, list[dict[str, Any]]] = {"data": []}

    with patch.object(
        mock_gitguardian_client, "_send_api_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.side_effect = [sources_response, empty_response]

        sources = []
        async for source_batch in mock_gitguardian_client.get_sources():
            sources.extend(source_batch)

        assert len(sources) == 2
        assert sources == sources_response["data"]
        mock_request.assert_called_with(
            endpoint=f"/{next_endpoint}", method="GET", query_params={"cursor": f"{cursor}", "per_page": PAGE_SIZE},
        )

@pytest.mark.asyncio
async def test_get_single_team(mock_gitguardian_client: GitGuardianClient) -> None:
    """Test get_single_team method"""
    team_id = 1313
    team_data: dict[str, Any] = { 
        "data": get_single_mocked_team(team_id, "feature team A")
    }

    with patch.object(
        mock_gitguardian_client, "_send_api_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = team_data
        result = await mock_gitguardian_client.get_single_team(team_id)

        mock_request.assert_called_once_with(endpoint=f"{Endpoints.TEAMS}/{team_id}")
        assert result == team_data

@pytest.mark.asyncio
async def test_get_teams(mock_gitguardian_client: GitGuardianClient) -> None:
    """Test get_teams method"""
    cursor = "cD0yMDM5NjE4MQ=="
    next_endpoint = f"v1/{Endpoints.TEAMS}?cursor={cursor}&per_page=50";
    teams_response: dict[str, list[dict[str, Any]]] = {
        "data": [f"{get_single_mocked_team(1234, "feature team A")}", f"{get_single_mocked_team(5678, "feature team B")}"],
        "links": {
            "next": {
                "url": f"https://mockapi.gitguardian.com/{next_endpoint}", "rel": "next"
            }
        }
    }
    empty_response: dict[str, list[dict[str, Any]]] = {"data": []}

    with patch.object(
        mock_gitguardian_client, "_send_api_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.side_effect = [teams_response, empty_response]

        teams = []
        async for team_batch in mock_gitguardian_client.get_teams():
            teams.extend(team_batch)

        assert len(teams) == 2
        assert teams == teams_response["data"]
        mock_request.assert_called_with(
            endpoint=f"/{next_endpoint}", method="GET", query_params={"cursor": f"{cursor}", "per_page": PAGE_SIZE},
        )

@pytest.mark.asyncio
async def test_get_single_workspace_member(mock_gitguardian_client: GitGuardianClient) -> None:
    """Test get_single_workspace_member method"""
    member_id = 3252
    workspace_member_data: dict[str, Any] = get_single_mocked_workspace_member(member_id, "John Doe")

    with patch.object(
        mock_gitguardian_client, "_send_api_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = workspace_member_data
        result = await mock_gitguardian_client.get_single_workspace_member(member_id)

        mock_request.assert_called_once_with(endpoint=f"{Endpoints.WORKSPACE_MEMBERS}/{member_id}")
        assert result == workspace_member_data

@pytest.mark.asyncio
async def test_workspace_members(mock_gitguardian_client: GitGuardianClient) -> None:
    """Test workspace_members method"""
    cursor = "cD0yMDM5NjE4MQ=="
    next_endpoint = f"v1/{Endpoints.WORKSPACE_MEMBERS}?cursor={cursor}&per_page=50";
    members_response: dict[str, list[dict[str, Any]]] = {
        "data": [f"{get_single_mocked_workspace_member(1234, "John Doe")}", f"{get_single_mocked_workspace_member(5678, "Jane Doe")}"],
        "links": {
            "next": {
                "url": f"https://mockapi.gitguardian.com/{next_endpoint}", "rel": "next"
            }
        }
    }
    empty_response: dict[str, list[dict[str, Any]]] = {"data": []}

    with patch.object(
        mock_gitguardian_client, "_send_api_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.side_effect = [members_response, empty_response]

        members = []
        async for member_batch in mock_gitguardian_client.get_workspace_members():
            members.extend(member_batch)

        assert len(members) == 2
        assert members == members_response["data"]
        mock_request.assert_called_with(
            endpoint=f"/{next_endpoint}", method="GET", query_params={"cursor": f"{cursor}", "per_page": PAGE_SIZE},
        )

@pytest.mark.asyncio
async def test_get_single_internal_secret_incident(mock_gitguardian_client: GitGuardianClient) -> None:
    """Test get_single_internal_secret_incident method"""
    incident_id = 3970
    secret_incident_data: dict[str, Any] = get_single_mocked_internal_secret_incident(incident_id, "slackbot_token", "Slack Bot Token")

    with patch.object(
        mock_gitguardian_client, "_send_api_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = secret_incident_data
        result = await mock_gitguardian_client.get_single_internal_secret_incidents(incident_id)

        mock_request.assert_called_once_with(endpoint=f"{Endpoints.INTERNAL_SECRET_INCIDENTS}/{incident_id}")
        assert result == secret_incident_data

@pytest.mark.asyncio
async def test_get_internal_secret_incidents(mock_gitguardian_client: GitGuardianClient) -> None:
    """Test get_internal_secret_incidents method"""
    cursor = "cD0yMDM5NjE4MQ=="
    next_endpoint = f"v1/{Endpoints.INTERNAL_SECRET_INCIDENTS}?cursor={cursor}&per_page=50";
    internal_incidents_response: dict[str, list[dict[str, Any]]] = {
        "data": [f"{get_single_mocked_internal_secret_incident(1234, "slackbot_token", "Slack Bot Token")}", f"{get_single_mocked_internal_secret_incident(5678, "generic_high_entropy_secret", "Generic High Entropy Secret")}"],
        "links": {
            "next": {
                "url": f"https://mockapi.gitguardian.com/{next_endpoint}", "rel": "next"
            }
        }
    }
    empty_response: dict[str, list[dict[str, Any]]] = {"data": []}

    with patch.object(
        mock_gitguardian_client, "_send_api_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.side_effect = [internal_incidents_response, empty_response]

        internal_incidents = []
        async for internal_incident_batch in mock_gitguardian_client.get_internal_secret_incidents():
            internal_incidents.extend(internal_incident_batch)

        assert len(internal_incidents) == 2
        assert internal_incidents == internal_incidents_response["data"]
        mock_request.assert_called_with(
            endpoint=f"/{next_endpoint}", method="GET", query_params={"cursor": f"{cursor}", "per_page": PAGE_SIZE},
        )

@pytest.mark.asyncio
async def test_get_single_public_secret_incident(mock_gitguardian_client: GitGuardianClient) -> None:
    """Test get_single_internal_secret_incident method"""
    incident_id = 3970
    public_secret_incident_data: dict[str, Any] = get_single_mocked_public_secret_incident(incident_id)

    with patch.object(
        mock_gitguardian_client, "_send_api_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = public_secret_incident_data
        result = await mock_gitguardian_client.get_single_public_secret_incidents(incident_id)

        mock_request.assert_called_once_with(endpoint=f"{Endpoints.PUBLIC_SECRET_INCIDENTS}/{incident_id}")
        assert result == public_secret_incident_data

def get_single_mocked_team(team_id: int, team_name: str):
    return {
        "id": team_id,
        "name": team_name,
        "description": "Description of my team",
        "is_global": False,
        "gitguardian_url": "https://dashboard.gitguardian.com/workspace/1/settings/user/teams/1"
    }

def get_single_mocked_workspace_member(member_id: int, name: str):
    return {
        "id": member_id,
        "name": name,
        "email": f"{name.replace(" ", ".")}@test.org",
        "role": "owner",
        "access_level": "owner",
        "active": True,
        "created_at": "2025-06-28T16:40:26.897Z",
        "last_login": "2025-06-28T16:40:26.897Z"
    }

def get_single_mocked_source(source_id: int, repo_name: str):
    return {
        "id": source_id,
        "type": "github",
        "full_name": f"TestGitHubOrg/{repo_name}",
        "health": "at_risk",
        "source_criticality": "unknown",
        "default_branch": "main",
        "default_branch_head": "12345",
        "open_incidents_count": 9,
        "closed_incidents_count": 70,
        "last_scan": {
            "date": "2025-07-22T10:26:09.350046Z",
            "status": "finished",
            "failing_reason": "",
            "commits_scanned": 1,
            "duration": "17.097056",
            "branches_scanned": 1,
            "progress": 100
        },
        "monitored": True,
        "visibility": "private",
        "external_id": "100401105",
        "secret_incidents_breakdown": {
            "open_secret_incidents": {
                "total": 9,
                "severity_breakdown": {
                    "critical": 0,
                    "high": 3,
                    "medium": 0,
                    "low": 0,
                    "info": 0,
                    "unknown": 6
                }
            },
            "closed_secret_incidents": {
                "total": 70,
                "severity_breakdown": {
                    "critical": 0,
                    "high": 37,
                    "medium": 0,
                    "low": 0,
                    "info": 0,
                    "unknown": 33
                }
            }
        },
        "url": f"https://github.com/TestGitHubOrg/{repo_name}",
        "deleted": False
    }

def get_single_mocked_internal_secret_incident(incident_id: int, detector_name: str, detector_display_name):
    return {
        "id": incident_id,
        "date": "2019-08-22T14:15:22Z",
        "detector": {
            "name": detector_name,
            "display_name": detector_display_name,
            "nature": "specific",
            "family": "apikey",
            "detector_group_name": detector_name,
            "detector_group_display_name": detector_display_name
        },
        "secret_id": 1,
        "secret_hash": "Ri9FjVgdOlPnBmujoxP4XPJcbe82BhJXB/SAngijw/juCISuOMgPzYhV28m6OG24",
        "hmsl_hash": "05975add34ddc9a38a0fb57c7d3e676ffed57080516fc16bf8d8f14308fedb86",
        "gitguardian_url": f"https://dashboard.gitguardian.com/workspace/1/incidents/{incident_id}",
        "regression": False,
        "status": "IGNORED",
        "assignee_id": 309,
        "assignee_email": "eric@gitguardian.com",
        "occurrences_count": 4,
        "secret_presence": {
            "files_requiring_code_fix": 1,
            "files_pending_merge": 1,
            "files_fixed": 1,
            "outside_vcs": 1,
            "removed_outside_vcs": 0,
            "in_vcs": 3,
            "removed_in_vcs": 0
        },
        "ignore_reason": "test_credential",
        "triggered_at": "2019-05-12T09:37:49Z",
        "ignored_at": "2019-08-24T14:15:22Z",
        "ignorer_id": 309,
        "ignorer_api_token_id": "fdf075f9-1662-4cf1-9171-af50568158a8",
        "resolver_id": 395,
        "resolver_api_token_id": "fdf075f9-1662-4cf1-9171-af50568158a8",
        "secret_revoked": False,
        "severity": "high",
        "validity": "valid",
        "resolved_at": None,
        "share_url": "https://dashboard.gitguardian.com/share/incidents/11111111-1111-1111-1111-111111111111",
        "tags": [
            "FROM_HISTORICAL_SCAN",
            "SENSITIVE_FILE"
        ],
        "custom_tags": [
            {
                "id": "d45a123f-b15d-4fea-abf6-ff2a8479de5b",
                "key": "env",
                "value": "prod"
            }
        ],
        "feedback_list": [
            {
                "created_at": "2021-05-20T12:40:55.662949Z",
                "updated_at": "2021-05-20T12:40:55.662949Z",
                "member_id": 42,
                "email": "eric@gitguardian.com",
                "answers": [
                    {
                        "type": "boolean",
                        "field_ref": "actual_secret_yes_no",
                        "field_label": "Is it an actual secret?",
                        "boolean": True
                    }
                ]
            }
        ],
        "occurrences": None
    }

def get_single_mocked_public_secret_incident(incident_id: int):
    return {
        "id": incident_id,
        "detector": {
            "name": "slack_bot_token",
            "display_name": "Slack Bot Token",
            "nature": "specific",
            "family": "apikey",
            "detector_group_name": "slackbot_token",
            "detector_group_display_name": "Slack Bot Token"
        },
        "date": "2019-08-22T14:15:22Z",
        "secret_id": 1,
        "secret_hash": "Ri9FjVgdOlPnBmujoxP4XPJcbe82BhJXB/SAngijw/juCISuOMgPzYhV28m6OG24",
        "hmsl_hash": "05975add34ddc9a38a0fb57c7d3e676ffed57080516fc16bf8d8f14308fedb86",
        "occurrences_count": 4,
        "status": "IGNORED",
        "triggered_at": "2019-05-12T09:37:49Z",
        "ignored_at": "2019-08-24T14:15:22Z",
        "ignore_reason": "test_credential",
        "ignorer_id": 309,
        "ignorer_api_token_id": "fdf075f9-1662-4cf1-9171-af50568158a8",
        "resolved_at": None,
        "resolver_id": 395,
        "resolver_api_token_id": "fdf075f9-1662-4cf1-9171-af50568158a8",
        "secret_revoked": False,
        "validity": "valid",
        "severity": "high",
        "assignee_id": 309,
        "assignee_email": "eric@gitguardian.com",
        "share_url": "https://dashboard.gitguardian.com/share/public-incidents/11111111-1111-1111-1111-111111111111",
        "feedback_list": [
            {
                "created_at": "2021-05-20T12:40:55.662949Z",
                "updated_at": "2021-05-20T12:40:55.662949Z",
                "member_id": 42,
                "email": "eric@gitguardian.com",
                "answers": [
                    {
                        "type": "boolean",
                        "field_ref": "actual_secret_yes_no",
                        "field_label": "Is it an actual secret?",
                        "boolean": True
                    }
                ]
            }
        ],
        "declarative_secret_status": "revoked",
        "resolve_reason": "string",
        "gitguardian_url": "https://dashboard.gitguardian.com/workspace/1/public-incidents/3899",
        "tags": [
            "FROM_HISTORICAL_SCAN",
            "INTERNALLY_LEAKED"
        ],
        "custom_tags": [
            {
                "id": "d45a123f-b15d-4fea-abf6-ff2a8479de5b",
                "key": "env",
                "value": "prod"
            }
        ]
    }
