from typing import Any, Optional
from gitguardian.overrides import (
    GitGuardianInternalSecretIncidentSelector,
    GitGuardianPublicSecretIncidentSelector,
    GitGuardianSecretDetectorSelector,
    GitGuardianSourceSelector,
    GitGuardianUserSelector,
)


def _produce_query_params(selector: Any, fields: list[str]) -> Optional[dict[str, Any]]:
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
    return _produce_query_params(selector, fields)


def produce_secret_detector_query_params(
    selector: GitGuardianSecretDetectorSelector,
) -> Optional[dict[str, Any]]:
    fields = [
        "is_active",
        "type",
        "search",
        "ordering",
    ]
    return _produce_query_params(selector, fields)


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
    return _produce_query_params(selector, fields)


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
    return _produce_query_params(selector, fields)


def produce_user_query_params(
    selector: GitGuardianUserSelector,
) -> Optional[dict[str, Any]]:
    fields = ["access_level", "active", "search", "ordering"]
    return _produce_query_params(selector, fields)
