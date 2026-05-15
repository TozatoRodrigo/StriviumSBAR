from app.enums.models.permissions_enums import (
    DoctorPermissionsEnum,
    HospitalizationPermissionsEnum,
    MedicalTeamPermissionsEnum,
    PatientPermissionsEnum,
    TenantUserPermissionsEnum,
)
from app.interfaces.seeders.seeder import Seeder
from app.models.permission import Permission


class PermissionSeeder(Seeder):
    def run(self) -> None:
        permissions = [
            # Tenant User
            Permission(
                code=TenantUserPermissionsEnum.CREATE.value,
                name="Criar usuários",
                description="Permite criar um usuário do sistema",
            ),
            Permission(
                code=TenantUserPermissionsEnum.READ.value,
                name="Listar usuários",
                description="Permite listar os usuários do sistema",
            ),
            Permission(
                code=TenantUserPermissionsEnum.UPDATE.value,
                name="Atualizar usuário",
                description="Permite atualizar um usuário do sistema",
            ),
            Permission(
                code=TenantUserPermissionsEnum.DELETE.value,
                name="Deletar usuário",
                description="Permite deletar um usuário do sistema",
            ),
            # Patient
            Permission(
                code=PatientPermissionsEnum.CREATE.value,
                name="Criar pacientes",
                description="Permite criar pacientes",
            ),
            Permission(
                code=PatientPermissionsEnum.READ.value,
                name="Listar pacientes",
                description="Permite listar pacientes",
            ),
            Permission(
                code=PatientPermissionsEnum.UPDATE.value,
                name="Atualizar pacientes",
                description="Permite atualizar pacientes",
            ),
            Permission(
                code=PatientPermissionsEnum.DELETE.value,
                name="Deletar pacientes",
                description="Permite deletar pacientes",
            ),
            # Hospitalization
            Permission(
                code=HospitalizationPermissionsEnum.CREATE.value,
                name="Criar internações",
                description="Permite criar internações",
            ),
            Permission(
                code=HospitalizationPermissionsEnum.READ.value,
                name="Listar internações",
                description="Permite listar internações",
            ),
            Permission(
                code=HospitalizationPermissionsEnum.UPDATE.value,
                name="Atualizar internações",
                description="Permite atualizar internações",
            ),
            Permission(
                code=HospitalizationPermissionsEnum.DELETE.value,
                name="Deletar internações",
                description="Permite deletar internações",
            ),
            # Medical Team
            Permission(
                code=MedicalTeamPermissionsEnum.CREATE.value,
                name="Criar equipes",
                description="Permite criar equipes médicas",
            ),
            Permission(
                code=MedicalTeamPermissionsEnum.READ.value,
                name="Listar equipes",
                description="Permite listar equipes médicas",
            ),
            Permission(
                code=MedicalTeamPermissionsEnum.UPDATE.value,
                name="Atualizar equipes",
                description="Permite atualizar equipes médicas",
            ),
            Permission(
                code=MedicalTeamPermissionsEnum.DELETE.value,
                name="Deletar equipes",
                description="Permite deletar equipes médicas",
            ),
            # Doctor
            Permission(
                code=DoctorPermissionsEnum.CREATE.value,
                name="Criar médicos",
                description="Permite criar médicos",
            ),
            Permission(
                code=DoctorPermissionsEnum.READ.value,
                name="Listar médicos",
                description="Permite listar médicos",
            ),
            Permission(
                code=DoctorPermissionsEnum.UPDATE.value,
                name="Atualizar médicos",
                description="Permite atualizar médicos",
            ),
            Permission(
                code=DoctorPermissionsEnum.DELETE.value,
                name="Deletar médicos",
                description="Permite deletar médicos",
            ),
        ]
        self.session.add_all(permissions)
