from typing import Literal
from port_ocean.core.handlers.port_app_config.models import (
    PortAppConfig,
    ResourceConfig,
    Selector,
)
from pydantic import Field


class SourceSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )

    
class SourceConfig(ResourceConfig):
    selector: SourceSelector
    kind: Literal["source"]


class SecretDetectorSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )

    
class SecretDetectorConfig(ResourceConfig):
    selector: SecretDetectorSelector
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


class TeamSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )


class TeamConfig(ResourceConfig):
    selector: TeamSelector
    kind: Literal["team"]


class MemberSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )


class MemberConfig(ResourceConfig):
    selector: MemberSelector
    kind: Literal["member"]


class DeveloperSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )


class DeveloperConfig(ResourceConfig):
    selector: DeveloperSelector
    kind: Literal["developer"]


class AuditLogSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )


class AuditLogConfig(ResourceConfig):
    selector: AuditLogSelector
    kind: Literal["audit_log"]


class CustomTagSelector(Selector):
    filter_query: str | None = None
    fields: str | None = Field(
        description="Additional fields to be included in the API response",
        default="*all",
    )


class CustomTagConfig(ResourceConfig):
    selector: CustomTagSelector
    kind: Literal["custom_tag"]


class GitGuardianPortAppConfig(PortAppConfig):
    resources: list[
        SourceConfig
        | SecretDetectorSelector
        | InternalSecretIncidentConfig
        | PublicSecretIncidentConfig
        | TeamConfig
        | MemberConfig
        | DeveloperConfig
        | AuditLogConfig
        | CustomTagConfig
        | ResourceConfig
    ]