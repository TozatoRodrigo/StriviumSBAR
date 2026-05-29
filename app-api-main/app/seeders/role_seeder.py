from app.enums.models.roles_names_enum import RolesNamesEnum
from app.interfaces.seeders.seeder import Seeder
from app.models.role import Role


class RoleSeeder(Seeder):
    def run(self) -> None:
        roles = [
            Role(
                name=RolesNamesEnum.ADMIN.value,
                description="Administrador do sistema",
            ),
            Role(
                name=RolesNamesEnum.DOCTOR.value,
                description="Médicos cadastrados no sistema",
            ),
        ]
        self.session.add_all(roles)
