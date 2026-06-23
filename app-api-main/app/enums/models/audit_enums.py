from enum import Enum, StrEnum


class AuditAction(StrEnum):
    """Sensitive actions tracked in the audit trail (LGPD Art. 46/48)."""

    LOGIN = "login"
    LOGIN_FAILED = "login_failed"
    LOGOUT = "logout"
    VIEW_PATIENT = "view:patient"
    CREATE_PATIENT = "create:patient"
    UPDATE_PATIENT = "update:patient"
    VIEW_HOSPITALIZATION = "view:hospitalization"
    CREATE_HOSPITALIZATION = "create:hospitalization"
    UPDATE_HOSPITALIZATION = "update:hospitalization"
    DELETE_HOSPITALIZATION = "delete:hospitalization"
    CREATE_HOSPITALIZATION_ACTION = "create:hospitalization_action"
    UPDATE_HOSPITALIZATION_ACTION = "update:hospitalization_action"
    CREATE_SBAR = "create:sbar"
    CREATE_TENANT_USER = "create:tenant_user"
    UPDATE_TENANT_USER = "update:tenant_user"
    DELETE_TENANT_USER = "delete:tenant_user"


class AuditResource(StrEnum):
    """Resource types referenced by audit entries."""

    AUTH = "auth"
    PATIENT = "patient"
    HOSPITALIZATION = "hospitalization"
    HOSPITALIZATION_ACTION = "hospitalization_action"
    SBAR = "sbar"
    TENANT_USER = "tenant_user"


class AuditLogPermissionsEnum(Enum):
    """Permissions controlling access to the audit trail."""

    READ = "read:audit_log"
