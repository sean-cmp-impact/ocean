from typing import Any, Optional
from gitguardian.overrides import GitGuardianAuditLogSelector


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
