from enum import Enum


class TenantUserPermissionsEnum(Enum):
    # Tenant User Permissions
    CREATE = "create:tenant_user"
    READ = "read:tenant_user"
    UPDATE = "update:tenant_user"
    DELETE = "delete:tenant_user"


class HospitalizationPermissionsEnum(Enum):
    # Hospitalization Permissions
    CREATE = "create:hospitalization"
    READ = "read:hospitalization"
    UPDATE = "update:hospitalization"
    DELETE = "delete:hospitalization"


class PatientPermissionsEnum(Enum):
    # Patient Permissions
    CREATE = "create:patient"
    READ = "read:patient"
    UPDATE = "update:patient"
    DELETE = "delete:patient"


class MedicalTeamPermissionsEnum(Enum):
    # Medical Team Permissions
    CREATE = "create:medical_team"
    READ = "read:medical_team"
    UPDATE = "update:medical_team"
    DELETE = "delete:medical_team"


class DoctorPermissionsEnum(Enum):
    # Doctor Permissions
    CREATE = "create:doctor"
    READ = "read:doctor"
    UPDATE = "update:doctor"
    DELETE = "delete:doctor"
