from typing import Any
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from port_ocean.context.ocean import initialize_port_ocean_context
from port_ocean.exceptions.context import PortOceanContextAlreadyInitializedError
from gitguardian.client import Endpoints, GitGuardianClient
from port_ocean.utils import http_async_client
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
        assert response["key"] == "value"

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
    source_data: dict[str, Any] = get_single_mocked_source()
    source_id = 123456789

    with patch.object(
        mock_gitguardian_client, "_send_api_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = source_data
        result = await mock_gitguardian_client.get_single_source(source_id)

        mock_request.assert_called_once_with(endpoint=f"{Endpoints.SOURCES}/{source_id}")
        assert result == source_data

def get_single_mocked_source():
    return {
        "id": 123456789,
        "type": "github",
        "full_name": "TestGitHubOrg/test_repo",
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
        "url": "https://github.com/TestGitHubOrg/test_repo",
        "deleted": False
    }