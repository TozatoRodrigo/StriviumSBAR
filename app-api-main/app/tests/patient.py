from faker import Faker

from app.core.database import get_session
from app.models.patient import Patient
from app.tests.tenant import create_tenant

fake = Faker()


def create_patient(data: dict | None = None) -> Patient:
    if data is None:
        data = {}
    tenant_id = data["tenant_id"] if "tenant_id" in data else create_tenant().id

    patient = Patient(
        tenant_id=tenant_id,
        first_name=data.get("first_name", fake.name()),
        last_name=data.get("last_name", fake.name()),
        document_number=data.get("document_number"),
        birth_date=data.get("birth_date", fake.date_of_birth()),
    )
    session = next(get_session())
    session.add(patient)
    session.commit()
    session.refresh(patient)
    session.close()
    return patient
