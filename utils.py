from typing import Any, Optional
from gitguardian.overrides import (
    GitGuardianAuditLogSelector,
    GitGuardianDeveloperSelector,
    GitGuardianInternalSecretIncidentSelector,
    GitGuardianPublicSecretIncidentSelector,
    GitGuardianSecretDetectorSelector,
    GitGuardianSourceSelector,
    GitGuardianTeamMemberSelector,
    GitGuardianTeamSelector,
    GitGuardianWorkspaceMemberSelector,
)


def produce_audit_log_query_params(
    selector: GitGuardianAuditLogSelector,
) -> Optional[dict[str, Any]]:
    fields = [
        "date_after",
        "date_before",
        "event_name",
        "member_id",
        "member_name",
        "member_email",
        "ip_address",
    ]
    query_params = {
        field: getattr(selector, field)
        for field in fields
        if getattr(selector, field) is not None and getattr(selector, field) != ""
    }
    return query_params or None


def produce_source_query_params(
    selector: GitGuardianSourceSelector,
) -> Optional[dict[str, Any]]:
    fields = [
        "search",
        "last_scan_status",
        "health",
        "type",
        "ordering",
        "visibility",
        "external_id",
        "source_criticality",
        "monitored",
    ]
    query_params = {
        field: getattr(selector, field)
        for field in fields
        if getattr(selector, field) is not None and getattr(selector, field) != ""
    }
    return query_params or None


def produce_secret_detector_query_params(
    selector: GitGuardianSecretDetectorSelector,
) -> Optional[dict[str, Any]]:
    fields = [
        "is_active",
        "type",
        "search",
        "ordering",
    ]
    query_params = {
        field: getattr(selector, field)
        for field in fields
        if getattr(selector, field) is not None and getattr(selector, field) != ""
    }
    return query_params or None


def produce_internal_secret_incidents_query_params(
    selector: GitGuardianInternalSecretIncidentSelector,
) -> Optional[dict[str, Any]]:
    fields = [
        "date_before",
        "date_after",
        "assignee_email",
        "assignee_id",
        "status",
        "severity",
        "validity",
        "tags",
        "custom_tags",
        "custom_tag_key",
        "custom_tag_value",
        "ordering",
        "detector_group_name",
        "ignorer_id",
        "resolver_id",
        "feedback",
    ]
    query_params = {
        field: getattr(selector, field)
        for field in fields
        if getattr(selector, field) is not None and getattr(selector, field) != ""
    }
    return query_params or None


def produce_public_secret_incidents_query_params(
    selector: GitGuardianPublicSecretIncidentSelector,
) -> Optional[dict[str, Any]]:
    fields = [
        "date_before",
        "date_after",
        "assignee_email",
        "assignee_id",
        "status",
        "severity",
        "validity",
        "tags",
        "custom_tags",
        "custom_tag_key",
        "custom_tag_value",
        "ordering",
        "detector_group_name",
        "ignorer_id",
        "resolver_id",
        "feedback",
        "declarative_secret_status",
    ]
    query_params = {
        field: getattr(selector, field)
        for field in fields
        if getattr(selector, field) is not None and getattr(selector, field) != ""
    }
    return query_params or None


def produce_team_query_params(
    selector: GitGuardianTeamSelector,
) -> Optional[dict[str, Any]]:
    fields = ["is_global", "search"]
    query_params = {
        field: getattr(selector, field)
        for field in fields
        if getattr(selector, field) is not None and getattr(selector, field) != ""
    }
    return query_params or None


def produce_workspace_member_query_params(
    selector: GitGuardianWorkspaceMemberSelector,
) -> Optional[dict[str, Any]]:
    fields = ["access_level", "active", "search", "ordering"]
    query_params = {
        field: getattr(selector, field)
        for field in fields
        if getattr(selector, field) is not None and getattr(selector, field) != ""
    }
    return query_params or None


def produce_team_member_query_params(
    selector: GitGuardianTeamMemberSelector,
) -> Optional[dict[str, Any]]:
    fields = ["is_team_leader", "incident_permission", "member_id"]
    query_params = {
        field: getattr(selector, field)
        for field in fields
        if getattr(selector, field) is not None and getattr(selector, field) != ""
    }
    return query_params or None


def produce_developer_query_params(
    selector: GitGuardianDeveloperSelector,
) -> Optional[dict[str, Any]]:
    fields = ["search", "ordering"]
    query_params = {
        field: getattr(selector, field)
        for field in fields
        if getattr(selector, field) is not None and getattr(selector, field) != ""
    }
    return query_params or None
