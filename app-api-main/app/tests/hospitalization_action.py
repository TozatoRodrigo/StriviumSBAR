from faker import Faker
from sqlmodel import Session

from app.core.database import engine
from app.models.hospitalization_action import (
    HospitalizationAction,
    HospitalizationActionStatus,
    HospitalizationActionType,
)
from app.tests.hospitalization import create_hospitalization
from app.tests.tenant import create_tenant

fake = Faker()


def create_hospitalization_action(data: dict | None = None) -> HospitalizationAction:
    data = data or {}
    tenant_id = data.get("tenant_id") or create_tenant().id
    hospitalization_id = data.get("hospitalization_id") or create_hospitalization().id
    status = data.get("status") or HospitalizationActionStatus.COMPLETED
    hospitalization_action_type = (
        data.get("hospitalization_action_type")
        or HospitalizationActionType.HOSPITALIZATION_VISIT
    )
    hospitalization_action = HospitalizationAction(
        tenant_id=tenant_id,
        hospitalization_id=hospitalization_id,
        user_id=data.get("user_id"),
        description=fake.sentence(2),
        status=status,
        type=hospitalization_action_type,
    )
    with Session(engine) as session:
        session.add(hospitalization_action)
        session.commit()
        session.refresh(hospitalization_action)
    return hospitalization_action
