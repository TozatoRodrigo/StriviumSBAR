from sqlmodel import select

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
            "admin": self.get_admin_permissions,
            "médico": self.get_doctor_permissions,
        }
        if role_name not in roles:
            return []

        return roles[role_name]()

    def get_admin_permissions(self) -> list[Permission]:
        permissions_codes = [
            "create:tenant_user",
            "read:tenant_user",
            "update:tenant_user",
            "delete:tenant_user",
        ]
        return self.session.exec(
            select(Permission).where(Permission.code.in_(permissions_codes))
        ).all()

    def get_doctor_permissions(self) -> list[Permission]:
        permissions_codes = []
        return self.session.exec(
            select(Permission).where(Permission.code.in_(permissions_codes))
        ).all()
