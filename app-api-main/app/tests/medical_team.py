from faker import Faker
from sqlmodel import Session as SQLModelSession

from app.core.database import engine
from app.models.medical_team import MedicalTeam
from app.tests.tenant import create_tenant

fake = Faker()


def create_medical_team(data: dict | None = None) -> MedicalTeam:
    if data is None:
        data = {}
    tenant_id = data["tenant_id"] if "tenant_id" in data else create_tenant().id

    medical_team = MedicalTeam(
        tenant_id=tenant_id,
        name=data["name"] if "name" in data else fake.name(),
        description=data["description"] if "description" in data else fake.text(),
    )
    with SQLModelSession(engine) as session:
        session.add(medical_team)
        session.commit()
        session.refresh(medical_team)
    return medical_team
