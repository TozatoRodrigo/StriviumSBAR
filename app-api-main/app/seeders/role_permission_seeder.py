from sqlmodel import select

from app.enums.models.permissions_enums import (
    DoctorPermissionsEnum,
    HospitalizationPermissionsEnum,
    MedicalTeamPermissionsEnum,
    PatientPermissionsEnum,
    TenantUserPermissionsEnum,
)
from app.enums.models.roles_names_enum import RolesNamesEnum
from app.interfaces.seeders.seeder import Seeder
from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission


class RolePermissionSeeder(Seeder):
    def run(self) -> None:
        roles = self.session.exec(select(Role)).all()
        for role in roles:
            permissions = self.get_role_permissions_by_role_name(role.name)
            role_permissions = []
            for permission in permissions:
                role_permission = RolePermission(
                    role_id=role.id, permission_id=permission.id
                )
                role_permissions.append(role_permission)
            self.session.add_all(role_permissions)

    def get_role_permissions_by_role_name(self, role_name: str) -> list[Permission]:
        roles = {
            RolesNamesEnum.ADMIN.value: self.get_admin_permissions,
            RolesNamesEnum.DOCTOR.value: self.get_doctor_permissions,
            # Backward compatibility for existing environments.
            "médico": self.get_doctor_permissions,
        }
        if role_name not in roles:
            return []

        return roles[role_name]()

    def get_admin_permissions(self) -> list[Permission]:
        permissions_codes = [
            TenantUserPermissionsEnum.CREATE.value,
            TenantUserPermissionsEnum.READ.value,
            TenantUserPermissionsEnum.UPDATE.value,
            TenantUserPermissionsEnum.DELETE.value,
            PatientPermissionsEnum.CREATE.value,
            PatientPermissionsEnum.READ.value,
            PatientPermissionsEnum.UPDATE.value,
            PatientPermissionsEnum.DELETE.value,
            HospitalizationPermissionsEnum.CREATE.value,
            HospitalizationPermissionsEnum.READ.value,
            HospitalizationPermissionsEnum.UPDATE.value,
            HospitalizationPermissionsEnum.DELETE.value,
            MedicalTeamPermissionsEnum.CREATE.value,
            MedicalTeamPermissionsEnum.READ.value,
            MedicalTeamPermissionsEnum.UPDATE.value,
            MedicalTeamPermissionsEnum.DELETE.value,
            DoctorPermissionsEnum.CREATE.value,
            DoctorPermissionsEnum.READ.value,
            DoctorPermissionsEnum.UPDATE.value,
            DoctorPermissionsEnum.DELETE.value,
        ]
        return self.session.exec(
            select(Permission).where(Permission.code.in_(permissions_codes))
        ).all()

    def get_doctor_permissions(self) -> list[Permission]:
        permissions_codes = [
            PatientPermissionsEnum.CREATE.value,
            PatientPermissionsEnum.READ.value,
            PatientPermissionsEnum.UPDATE.value,
            HospitalizationPermissionsEnum.CREATE.value,
            HospitalizationPermissionsEnum.READ.value,
            HospitalizationPermissionsEnum.UPDATE.value,
            MedicalTeamPermissionsEnum.READ.value,
            DoctorPermissionsEnum.READ.value,
        ]
        return self.session.exec(
            select(Permission).where(Permission.code.in_(permissions_codes))
        ).all()
