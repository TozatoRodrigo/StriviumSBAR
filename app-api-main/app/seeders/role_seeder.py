from app.interfaces.seeders.seeder import Seeder
from app.models.role import Role


class RoleSeeder(Seeder):
    def run(self) -> None:
        roles = [
            Role(name="admin", description="Administrador do sistema"),
            Role(name="médico", description="Médicos cadastrados no sistema"),
        ]
        self.session.add_all(roles)
