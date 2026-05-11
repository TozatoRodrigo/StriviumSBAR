from faker import Faker
from sqlmodel import Session as SQLModelSession

from app.core.database import engine
from app.models.hospitalization import Hospitalization, HospitalizationStatus
from app.tests.medical_team import create_medical_team
from app.tests.patient import create_patient
from app.tests.tenant import create_tenant
from app.tests.user import create_user

fake = Faker()


def create_hospitalization(data: dict | None = None) -> Hospitalization:
    if data is None:
        data = {}
    tenant_id = data["tenant_id"] if "tenant_id" in data else create_tenant().id
    user_id = data["user_id"] if "user_id" in data else create_user().id
    patient_id = data["patient_id"] if "patient_id" in data else create_patient().id
    medical_team_id = (
        data["medical_team_id"]
        if "medical_team_id" in data
        else create_medical_team().id
    )

    hospitalization = Hospitalization(
        tenant_id=tenant_id,
        user_id=user_id,
        patient_id=patient_id,
        medical_team_id=medical_team_id,
        status=data.get("status", HospitalizationStatus.ACTIVE),
        hospitalization_number=data.get(
            "hospitalization_number", fake.numerify("####")
        ),
        hospitalization_place=data.get("hospitalization_place"),
        hospitalization_sector=data.get(
            "hospitalization_sector", fake.text(max_nb_chars=10)
        ),
        hospitalization_reason=data.get(
            "hospitalization_reason", fake.text(max_nb_chars=20)
        ),
        observation=data.get("observation", fake.text(max_nb_chars=20)),
    )
    with SQLModelSession(engine) as session:
        session.add(hospitalization)
        session.commit()
        session.refresh(hospitalization)
        session.close()
    return hospitalization
