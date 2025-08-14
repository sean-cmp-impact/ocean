from typing import Any, Literal, Optional
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


class GitGuardianInternalSecretIncidentSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )


class GitGuardianInternalSecretIncidentConfig(ResourceConfig):
    selector: GitGuardianInternalSecretIncidentSelector
    kind: Literal["internal_secret_incident"]


class GitGuardianPublicSecretIncidentSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )


class GitGuardianPublicSecretIncidentConfig(ResourceConfig):
    selector: GitGuardianPublicSecretIncidentSelector
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
    date_before: str | None = Field(
        description="Audit log entries found before this date. Example: 2025-08-15T14:15:22Z",
    )
    date_after: str | None = Field(
        description="Audit log entries found after this date. Example: 2025-08-15T14:15:22Z",
    )
    event_name: str | None = Field(
        description="Audit log entries matching this event name. Example: user.logged_in",
    )
    member_id: Optional[int] | None = Field(
        description="Audit log entries to retrieve for the specified member id. Example: 3252",
    )
    member_name: str | None = Field(
        description="Audit log entries matching this member name. Example: John Smith",
    )
    member_email: str | None = Field(
        description="Audit log entries matching this member email. Example: john.smith@example.org",
    )
    ip_address: str | None = Field(
        description="Audit log entries matching this IP address. Example: 8.8.8.8",
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
        | GitGuardianInternalSecretIncidentConfig
        | GitGuardianPublicSecretIncidentConfig
        | GitGuardianTeamConfig
        | GitGuardianWorkspaceMemberConfig
        | GitGuardianTeamMemberConfig
        | GitGuardianDeveloperConfig
        | GitGuardianAuditLogConfig
        | GitGuardianCustomTagConfig
        | ResourceConfig
    ]
