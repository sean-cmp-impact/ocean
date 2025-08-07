from typing import Literal
from port_ocean.core.handlers.port_app_config.models import (
    PortAppConfig,
    ResourceConfig,
    Selector,
)
from pydantic import Field


class GitGuardianSourceSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )

    
class GitGuardianSourceConfig(ResourceConfig):
    selector: GitGuardianSourceSelector
    kind: Literal["source"]


class GitGuardianSecretDetectorSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )

    
class GitGuardianSecretDetectorConfig(ResourceConfig):
    selector: GitGuardianSecretDetectorSelector
    kind: Literal["secret_detector"]


class InternalSecretIncidentSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )
    

class InternalSecretIncidentConfig(ResourceConfig):
    selector: InternalSecretIncidentSelector
    kind: Literal["internal_secret_incident"]


class PublicSecretIncidentSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )
    

class PublicSecretIncidentConfig(ResourceConfig):
    selector: PublicSecretIncidentSelector
    kind: Literal["public_secret_incident"]


class GitGuardianTeamSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )


class GitGuardianTeamConfig(ResourceConfig):
    selector: GitGuardianTeamSelector
    kind: Literal["team"]


class GitGuardianWorkspaceMemberSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )


class GitGuardianWorkspaceMemberConfig(ResourceConfig):
    selector: GitGuardianWorkspaceMemberSelector
    kind: Literal["workspace_member"]


class GitGuardianTeamMemberSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )


class GitGuardianTeamMemberConfig(ResourceConfig):
    selector: GitGuardianTeamMemberSelector
    kind: Literal["team_member"]


class GitGuardianDeveloperSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )


class GitGuardianDeveloperConfig(ResourceConfig):
    selector: GitGuardianDeveloperSelector
    kind: Literal["developer"]


class GitGuardianAuditLogSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )


class GitGuardianAuditLogConfig(ResourceConfig):
    selector: GitGuardianAuditLogSelector
    kind: Literal["audit_log"]


class GitGuardianCustomTagSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )


class GitGuardianCustomTagConfig(ResourceConfig):
    selector: GitGuardianCustomTagSelector
    kind: Literal["custom_tag"]


class GitGuardianPortAppConfig(PortAppConfig):
    resources: list[
        GitGuardianSourceConfig
        | GitGuardianSecretDetectorSelector
        | InternalSecretIncidentConfig
        | PublicSecretIncidentConfig
        | GitGuardianTeamConfig
        | GitGuardianWorkspaceMemberConfig
        | GitGuardianTeamMemberConfig
        | GitGuardianDeveloperConfig
        | GitGuardianAuditLogConfig
        | GitGuardianCustomTagConfig
        | ResourceConfig
    ]