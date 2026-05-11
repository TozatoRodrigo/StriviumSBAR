from sqlmodel import Session

from app.core.database import engine
from app.models.medical_team_user import MedicalTeamUser
from app.tests.medical_team import create_medical_team
from app.tests.tenant import create_tenant
from app.tests.user import create_user


def create_medical_team_user(data: dict | None = None) -> MedicalTeamUser:
    if data is None:
        data = {}
    medical_team_user = MedicalTeamUser(
        tenant_id=data.get("tenant_id", create_tenant().id),
        medical_team_id=data.get("medical_team_id", create_medical_team().id),
        user_id=data.get("user_id", create_user().id),
    )
    with Session(engine) as session:
        session.add(medical_team_user)
        session.commit()
        session.refresh(medical_team_user)
    return medical_team_user
