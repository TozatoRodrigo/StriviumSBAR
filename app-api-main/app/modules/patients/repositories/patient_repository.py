from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlmodel import paginate
from sqlmodel import Session, or_, select

from app.models.patient import Patient
from app.utils.uuid import is_valid_uuid


class PatientRepository:
    def __init__(self, session: Session, tenant_id: UUID) -> None:
        self.session = session
        self.tenant_id = tenant_id

    def save(self, patient: Patient) -> Patient:
        self.session.add(patient)
        self.session.commit()
        self.session.refresh(patient)
        return patient

    def find_by_id(self, patient_id: UUID) -> Patient | None:
        return self.session.exec(
            select(Patient).where(
                Patient.id == patient_id,
                Patient.tenant_id == self.tenant_id,
            )
        ).first()

    def paginate(self, page: int, limit: int, search: str | None) -> Page[Patient]:
        query = (
            select(Patient)
            .where(Patient.tenant_id == self.tenant_id)
            .order_by(Patient.first_name.asc())
        )
        if search:
            conditions = [
                Patient.first_name.ilike(f"%{search}%"),
                Patient.last_name.ilike(f"%{search}%"),
            ]

            if is_valid_uuid(search):
                conditions.append(Patient.id == UUID(search))

            query = query.where(or_(*conditions))

        return paginate(
            self.session,
            query,
            Params(page=page, size=limit),
        )
