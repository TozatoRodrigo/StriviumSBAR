from datetime import datetime, time
from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlmodel import paginate
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlmodel import Session, exists, not_, or_, select
from sqlmodel.sql.expression import SelectOfScalar

from app.enums.models.hospitalization_status_enums import HospitalizationStatus
from app.models.hospitalization import Hospitalization
from app.models.hospitalization_action import HospitalizationAction
from app.models.medical_team import MedicalTeam
from app.models.patient import Patient
from app.utils.timezone import get_timezone


class HospitalizationRepository:
    def __init__(self, session: Session, tenant_id: UUID) -> None:
        self.session = session
        self.tenant_id = tenant_id

    def save(self, hospitalization: Hospitalization) -> Hospitalization:
        self.session.add(hospitalization)
        self.session.commit()
        self.session.refresh(hospitalization)
        return hospitalization

    def update(self, hospitalization: Hospitalization) -> Hospitalization:
        self.session.add(hospitalization)
        self.session.commit()
        self.session.refresh(hospitalization)
        return hospitalization

    def paginate(
        self,
        page: int,
        limit: int,
        patient_id: UUID | None = None,
        search: str | None = None,
    ) -> Page[Hospitalization]:
        query = (
            select(Hospitalization)
            .where(Hospitalization.tenant_id == self.tenant_id)
            .options(joinedload(Hospitalization.patient))
        )
        if patient_id:
            query = query.where(Hospitalization.patient_id == patient_id)
        if search:
            query = self.__apply_search(query, search)
        return paginate(self.session, query, Params(page=page, size=limit))

    def get(self, hospitalization_id: UUID) -> Hospitalization:
        query = (
            select(Hospitalization)
            .where(
                Hospitalization.id == hospitalization_id,
                Hospitalization.tenant_id == self.tenant_id,
            )
            .options(joinedload(Hospitalization.patient))
        )
        return self.session.exec(query).first()

    def is_medical_team_in_tenant(self, medical_team_id: UUID) -> bool:
        query = select(MedicalTeam.id).where(
            MedicalTeam.id == medical_team_id,
            MedicalTeam.tenant_id == self.tenant_id,
        )
        return self.session.exec(query).first() is not None

    @staticmethod
    def _get_today_start() -> datetime:
        return datetime.combine(
            datetime.now(get_timezone()).date(),
            time.min,
        ).replace(tzinfo=get_timezone())

    def paginate_pendings(
        self, page: int, limit: int, search: str | None = None
    ) -> Page[Hospitalization]:
        query = (
            select(Hospitalization)
            .where(
                Hospitalization.tenant_id == self.tenant_id,
                Hospitalization.status == HospitalizationStatus.ACTIVE,
                not_(
                    exists().where(
                        HospitalizationAction.hospitalization_id == Hospitalization.id,
                        HospitalizationAction.created_at >= self._get_today_start(),
                    )
                ),
            )
            .options(joinedload(Hospitalization.patient))
        )
        if search:
            query = self.__apply_search(query, search)
        return paginate(self.session, query, Params(page=page, size=limit))

    def paginate_completed(
        self, page: int, limit: int, search: str | None = None
    ) -> Page[Hospitalization]:
        query = (
            select(Hospitalization)
            .where(
                Hospitalization.tenant_id == self.tenant_id,
                Hospitalization.status == HospitalizationStatus.ACTIVE,
                exists().where(
                    HospitalizationAction.hospitalization_id == Hospitalization.id,
                    HospitalizationAction.created_at >= self._get_today_start(),
                ),
            )
            .options(joinedload(Hospitalization.patient))
        )
        if search:
            query = self.__apply_search(query, search)
        return paginate(self.session, query, Params(page=page, size=limit))

    @staticmethod
    def __apply_search(
        query: SelectOfScalar[Hospitalization], search: str
    ) -> SelectOfScalar[Hospitalization]:
        return query.join(Hospitalization.patient).where(
            or_(
                Hospitalization.hospitalization_number.ilike(f"%{search}%"),
                Hospitalization.hospitalization_place.ilike(f"%{search}%"),
                Hospitalization.hospitalization_sector.ilike(f"%{search}%"),
                Hospitalization.hospitalization_reason.ilike(f"%{search}%"),
                func.concat(Patient.first_name, " ", Patient.last_name).ilike(
                    f"%{search}%"
                ),
            )
        )
