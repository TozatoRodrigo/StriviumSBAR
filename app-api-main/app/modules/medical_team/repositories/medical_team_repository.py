from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlmodel import paginate
from sqlalchemy.orm import selectinload
from sqlmodel import Session, delete, or_, select

from app.models.medical_team import MedicalTeam
from app.models.medical_team_user import MedicalTeamUser


class MedicalTeamRepository:
    def __init__(self, db: Session, tenant_id: UUID) -> None:
        self.db = db
        self.tenant_id = tenant_id

    def save(self, medical_team: MedicalTeam) -> MedicalTeam:
        self.db.add(medical_team)
        self.db.commit()
        self.db.refresh(medical_team)
        return medical_team

    def paginate(self, page: int, limit: int, search: str | None) -> Page[MedicalTeam]:
        query = select(MedicalTeam).where(MedicalTeam.tenant_id == self.tenant_id)
        if search:
            query = query.where(
                or_(
                    MedicalTeam.name.ilike(f"%{search}%"),
                    MedicalTeam.description.ilike(f"%{search}%"),
                ),
            )
        return paginate(self.db, query, Params(page=page, size=limit))

    def show_by_id_and_tenant_id(
        self, medical_team_id: UUID, tenant_id: UUID
    ) -> MedicalTeam | None:
        query = (
            select(MedicalTeam)
            .where(
                MedicalTeam.id == medical_team_id, MedicalTeam.tenant_id == tenant_id
            )
            .options(
                selectinload(MedicalTeam.medical_team_users).joinedload(
                    MedicalTeamUser.user
                )
            )
        )
        return self.db.exec(query).first()

    def delete(self, medical_team_id: UUID) -> None:
        self.db.exec(delete(MedicalTeam).where(MedicalTeam.id == medical_team_id))
        self.db.commit()

    def get_by_id(self, medical_team_id: UUID) -> MedicalTeam | None:
        return self.db.exec(
            select(MedicalTeam).where(
                MedicalTeam.id == medical_team_id,
                MedicalTeam.tenant_id == self.tenant_id,
            )
        ).first()
