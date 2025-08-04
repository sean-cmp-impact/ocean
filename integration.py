from enum import StrEnum
from port_ocean.core.handlers.port_app_config.api import APIPortAppConfig
from port_ocean.core.integrations.base import BaseIntegration

from gitguardian.overrides import GitGuardianPortAppConfig


class ObjectKind(StrEnum):
    SOURCE = "source"
    SECRET_DETECTOR = "secret_detector"
    INTERNAL_SECRET_INCIDENT = "internal_secret_incident"
    PUBLIC_SECRET_INCIDENT = "public_secret_incident"
    TEAM = "team"
    MEMBER = "member"
    DEVELOPER = "member"
    AUDIT_LOG = "audit_log"
    CUSTOM_TAG = "custom_tag"


class GitGuardianIntegration(BaseIntegration):
    class AppConfigHandlerClass(APIPortAppConfig):
        CONFIG_CLASS = GitGuardianPortAppConfig