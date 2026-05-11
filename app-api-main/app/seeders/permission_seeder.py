from app.interfaces.seeders.seeder import Seeder
from app.models.permission import Permission


class PermissionSeeder(Seeder):
    def run(self) -> None:
        permissions = [
            # Tenant User
            Permission(
                code="create:tenant_user",
                name="Criar usuários",
                description="Permite criar um usuário do sistema",
            ),
            Permission(
                code="read:tenant_user",
                name="Listar usuários",
                description="Permite listar os usuários do sistema",
            ),
            Permission(
                code="update:tenant_user",
                name="Atualizar usuário",
                description="Permite atualizar um usuário do sistema",
            ),
            Permission(
                code="delete:tenant_user",
                name="Deletar usuário",
                description="Permite deletar um usuário do sistema",
            ),
        ]
        self.session.add_all(permissions)
