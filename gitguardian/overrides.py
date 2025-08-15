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
    date_before: str | None = Field(
        description="Return internal secret incident entries found before this date. Example value: 2025-08-15T14:15:22Z"
    )
    date_after: str | None = Field(
        description="Return internal secret incident entries found after this date. Example value: 2025-08-15T14:15:22Z"
    )
    assignee_email: str | None = Field(
        description="Filter internal secret incidents assigned to this email. Example value: user@example.com"
    )
    assignee_id: Optional[int] | None = Field(
        description="Filter internal secret incidents assigned to this user ID. Example value: 4932"
    )
    status: str | None = Field(
        description="Filter internal secret incidents by their status. Available values include: IGNORED, TRIGGERED, ASSIGNED, and RESOLVED"
    )
    severity: str | None = Field(
        description="Filter internal secret incidents by their severity. Available values include: critical, high, medium, low, info, and unknown"
    )
    validity: str | None = Field(
        description="Filter internal secret incidents by their validity status. Available values include: valid, invalid, failed_to_check, no_checker, and unknown"
    )
    tags: str | None = Field(
        description="Filter internal secret incidents with tags. Example of comma separated value: FROM_HISTORICAL_SCAN,SENSITIVE_FILE. Alternatively, use NONE if you want to filter incidents with no tags. All available values include: DEFAULT_BRANCH,FROM_HISTORICAL_SCAN,CHECK_RUN_SKIP_FALSE_POSITIVE,CHECK_RUN_SKIP_LOW_RISK,CHECK_RUN_SKIP_TEST_CRED,PUBLIC,PUBLICLY_EXPOSED,PUBLICLY_LEAKED,REGRESSION,SENSITIVE_FILE,TEST_FILE,FALSE_POSITIVE,VAULTED, and NONE"
    )
    custom_tags: str | None = Field(
        description="Filter internal secret incidents with custom tags. Example value: d45a123f-b15d-4fea-abf6-ff2a8479de5b,55b349d7-8c3a-40c9-957c-e58f5c3a7391"
    )
    custom_tag_key: str | None = Field(
        description="Filter internal secret incidents with a specific custom tag key. Example value: environment"
    )
    custom_tag_value: str | None = Field(
        description="Filter internal secret incidents with a specific custom tag value. Example value: production"
    )
    ordering: str | None = Field(
        description="Sort the results by their field value. The default sort is ASC, DESC if the field is preceded by a '-'. Available filter values include: date, -date, resolved_at, -resolved_at, ignored_at, and -ignored_at"
    )
    detector_group_name: str | None = Field(
        description="Filter internal secret incidents belonging to the specified detector group. Example value: slackbot_token"
    )
    ignorer_id: Optional[int] | None = Field(
        description="Filter internal secret incidents ignored by this user ID. Example value: 4932"
    )
    resolver_id: str | None = Field(
        description="Filter internal secret incidents resolved by this user ID. Example value: 4932"
    )
    feedback: bool | None = Field(
        description="Filter internal secret incidents with or without feedback. Available values include: true and false"
    )


class GitGuardianInternalSecretIncidentConfig(ResourceConfig):
    selector: GitGuardianInternalSecretIncidentSelector
    kind: Literal["internal_secret_incident"]


class GitGuardianPublicSecretIncidentSelector(Selector):
    date_before: str | None = Field(
        description="Return public secret incident entries found before this date. Example value: 2025-08-15T14:15:22Z"
    )
    date_after: str | None = Field(
        description="Return public secret incident entries found after this date. Example value: 2025-08-15T14:15:22Z"
    )
    assignee_email: str | None = Field(
        description="Filter public secret incidents assigned to this email. Example value: user@example.com"
    )
    assignee_id: Optional[int] | None = Field(
        description="Filter public secret incidents assigned to this user ID. Example value: 4932"
    )
    status: str | None = Field(
        description="Filter public secret incidents by their status. Available values include: IGNORED, TRIGGERED, ASSIGNED, and RESOLVED"
    )
    severity: str | None = Field(
        description="Filter public secret incidents by their severity. Available values include: critical, high, medium, low, info, and unknown"
    )
    validity: str | None = Field(
        description="Filter public secret incidents by their validity status. Available values include: valid, invalid, failed_to_check, no_checker, and unknown"
    )
    tags: str | None = Field(
        description="Filter public secret incidents with tags. Example of comma separated value: FROM_HISTORICAL_SCAN,SENSITIVE_FILE. Alternatively, use NONE if you want to filter incidents with no tags. All available values include: DEFAULT_BRANCH,FROM_HISTORICAL_SCAN,CHECK_RUN_SKIP_FALSE_POSITIVE,CHECK_RUN_SKIP_LOW_RISK,CHECK_RUN_SKIP_TEST_CRED,PUBLIC,PUBLICLY_EXPOSED,PUBLICLY_LEAKED,REGRESSION,SENSITIVE_FILE,TEST_FILE,FALSE_POSITIVE,VAULTED, and NONE"
    )
    custom_tags: str | None = Field(
        description="Filter public secret incidents with custom tags. Example value: d45a123f-b15d-4fea-abf6-ff2a8479de5b,55b349d7-8c3a-40c9-957c-e58f5c3a7391"
    )
    custom_tag_key: str | None = Field(
        description="Filter public secret incidents with a specific custom tag key. Example value: environment"
    )
    custom_tag_value: str | None = Field(
        description="Filter public secret incidents with a specific custom tag value. Example value: production"
    )
    ordering: str | None = Field(
        description="Sort the results by their field value. The default sort is ASC, DESC if the field is preceded by a '-'. Available filter values include: date, -date, resolved_at, -resolved_at, ignored_at, and -ignored_at"
    )
    detector_group_name: str | None = Field(
        description="Filter public secret incidents belonging to the specified detector group. Example value: slackbot_token"
    )
    ignorer_id: Optional[int] | None = Field(
        description="Filter public secret incidents ignored by this user ID. Example value: 4932"
    )
    resolver_id: str | None = Field(
        description="Filter public secret incidents resolved by this user ID. Example value: 4932"
    )
    feedback: bool | None = Field(
        description="Filter public secret incidents with or without feedback. Available values include: true and false"
    )
    declarative_secret_status: str | None = Field(
        description="Filter public secret incidents by their declarative secret status. Available values include: revoked, active, test_credential, false_positive, and low_risk"
    )


class GitGuardianPublicSecretIncidentConfig(ResourceConfig):
    selector: GitGuardianPublicSecretIncidentSelector
    kind: Literal["public_secret_incident"]


class GitGuardianTeamSelector(Selector):
    is_global: bool | None = Field(
        description="Filter on/exclude the 'All-incidents' team. Available filter values include: true and false"
    )
    search: str | None = Field(
        description="Search teams based on their name and/or description. Example value: finance"
    )


class GitGuardianTeamConfig(ResourceConfig):
    selector: GitGuardianTeamSelector
    kind: Literal["team"]


class GitGuardianWorkspaceMemberSelector(Selector):
    access_level: str | None = Field(
        description="Filter members based on their access level. Available filter values include: owner, manager, member, and restricted"
    )
    active: bool | None = Field(
        description="Filter members based on their active status. Available filter values include: true and false"
    )
    search: str | None = Field(
        description="Search members based on their name or email. Example value: John Smith or john.smith@example.com"
    )
    ordering: str | None = Field(
        description="Sort the results by their field value. The default sort is ASC, DESC if the field is preceded by a '-'. Available filter values include: created_at, -created_at, last_login, and -last_login"
    )


class GitGuardianWorkspaceMemberConfig(ResourceConfig):
    selector: GitGuardianWorkspaceMemberSelector
    kind: Literal["workspace_member"]


class GitGuardianTeamMemberSelector(Selector):
    team_id: int = Field(
        description="Filter team memberships for a specific team ID. Example value: 5678"
    )
    is_team_leader: bool | None = Field(
        description="Filter team memberships that are team leaders. Available filter values include: true and false"
    )
    incident_permission: str | None = Field(
        description="Filter team memberships with a specific team permission. Available filter values include: can_manage and cannot_manage"
    )
    member_id: Optional[int] | None = Field(
        description="Filter team memberships for a specific member ID. Example value: 1234"
    )


class GitGuardianTeamMemberConfig(ResourceConfig):
    selector: GitGuardianTeamMemberSelector
    kind: Literal["team_member"]


class GitGuardianDeveloperSelector(Selector):
    search: str | None = Field(description="Search developers matching this search.")
    ordering: str | None = Field(
        description="Sort the results by their field value. The default sort is ASC, DESC if the field is preceded by a '-'. Available filter values include: github_login, -github_login, name, -name, emails, -emails, is_active, and -is_active"
    )


class GitGuardianDeveloperConfig(ResourceConfig):
    selector: GitGuardianDeveloperSelector
    kind: Literal["developer"]


class GitGuardianAuditLogSelector(Selector):
    date_before: str | None = Field(
        description="Audit log entries found before this date. Example value: 2025-08-15T14:15:22Z"
    )
    date_after: str | None = Field(
        description="Audit log entries found after this date. Example value: 2025-08-15T14:15:22Z"
    )
    event_name: str | None = Field(
        description="Audit log entries matching this event name. Example value: user.logged_in"
    )
    member_id: Optional[int] | None = Field(
        description="Audit log entries to retrieve for the specified member id. Example value: 3252"
    )
    member_name: str | None = Field(
        description="Audit log entries matching this member name. Example value: John Smith"
    )
    member_email: str | None = Field(
        description="Audit log entries matching this member email. Example value: john.smith@example.org"
    )
    ip_address: str | None = Field(
        description="Audit log entries matching this IP address. Example value: 8.8.8.8"
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
