from typing import Literal, Optional
from port_ocean.core.handlers.port_app_config.models import (
    PortAppConfig,
    ResourceConfig,
    Selector,
)
from pydantic import Field


class GitGuardianSourceSelector(Selector):
    search: str | None = Field(
        description="Returns sources matching this search. Example value: test-repository"
    )
    last_scan_status: str | None = Field(
        description="Filter sources based on the status of their latest historical scan. Available filter values include: pending, running, canceled, failed, too_large, timeout, pending_timeout, and finished"
    )
    health: str | None = Field(
        description="Filter sources based on their health status. Available filter values include: safe, unknown, and at_risk"
    )
    type: str | None = Field(
        description="Filter sources based on their integration type. Available filter values include: bitbucket, bitbucket_cloud, github, gitlab, azure_devops, slack, jira_cloud, confluence_cloud, microsoft_teams, confluence_data_center, jira_data_center, servicenow, sharepoint_online, sharepoint_online_drive, sharepoint_online_pages"
    )
    ordering: str | None = Field(
        description="Sort the results by their field value. The default sort is ASC, DESC if the field is preceded by a '-'. Available filter values include: last_scan_date and -last_scan_date"
    )
    visibility: str | None = Field(
        description="Filter sources based on their visibility status. Available filter values include: public, private, and internal"
    )
    external_id: str | None = Field(
        description="Filter sources based on their external ID. Example value: 1"
    )
    source_criticality: str | None = Field(
        description="Filter sources based on their criticality level. Available filter values include: critical, high, medium, low, and unknown"
    )
    monitored: bool | None = Field(
        description="Filter sources by monitored value. Available filter values include: true, false"
    )


class GitGuardianSourceConfig(ResourceConfig):
    selector: GitGuardianSourceSelector
    kind: Literal["source"]


class GitGuardianSecretDetectorSelector(Selector):
    is_active: bool | None = Field(
        description="Filter only active or inactive detectors. Available filter values include: true, false"
    )
    type: str | None = Field(
        description="Filter detectors on their type. Available filter values include: specific generic custom"
    )
    search: str | None = Field(
        description="Returns detectors matching this search filter. Example value: aws"
    )
    ordering: str | None = Field(
        description="Sort the results by their field value. The default sort is ASC, DESC if the field is preceded by a '-'. Available filter values include: name and -name"
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
        description="Audit log entries found before this date. Example value: 2025-08-15T14:15:22Z",
    )
    date_after: str | None = Field(
        description="Audit log entries found after this date. Example value: 2025-08-15T14:15:22Z",
    )
    event_name: str | None = Field(
        description="Audit log entries matching this event name. Example value: user.logged_in",
    )
    member_id: Optional[int] | None = Field(
        description="Audit log entries to retrieve for the specified member id. Example value: 3252",
    )
    member_name: str | None = Field(
        description="Audit log entries matching this member name. Example value: John Smith",
    )
    member_email: str | None = Field(
        description="Audit log entries matching this member email. Example value: john.smith@example.org",
    )
    ip_address: str | None = Field(
        description="Audit log entries matching this IP address. Example value: 8.8.8.8",
    )


class GitGuardianAuditLogConfig(ResourceConfig):
    selector: GitGuardianAuditLogSelector
    kind: Literal["audit_log"]


class GitGuardianCustomTagSelector(Selector):
    key: str | None = Field(
        description="Filter on the specified custom tag key. Example value: env",
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
