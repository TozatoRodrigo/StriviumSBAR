from uuid import UUID

from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlmodel import paginate
from sqlalchemy.orm import joinedload, selectinload, with_loader_criteria
from sqlmodel import Session, select

from app.models.hospitalization_action import HospitalizationAction
from app.models.tenant_user import TenantUser
from app.models.user import User


class HospitalizationActionRepository:
    def __init__(self, session: Session, tenant_id: UUID) -> None:
        self.session = session
        self.tenant_id = tenant_id

    def create(
        self, hospitalization_action: HospitalizationAction
    ) -> HospitalizationAction:
        self.session.add(hospitalization_action)
        self.session.commit()
        self.session.refresh(hospitalization_action)
        return hospitalization_action

    def update(
        self, hospitalization_action: HospitalizationAction
    ) -> HospitalizationAction:
        self.session.add(hospitalization_action)
        self.session.commit()
        self.session.refresh(hospitalization_action)
        return hospitalization_action

    def find_by_id(
        self, hospitalization_action_id: UUID
    ) -> HospitalizationAction | None:
        return self.session.exec(
            select(HospitalizationAction)
            .where(
                HospitalizationAction.id == hospitalization_action_id,
                HospitalizationAction.tenant_id == self.tenant_id,
            )
            .options(
                joinedload(HospitalizationAction.user)
                .selectinload(User.tenant_users)
                .load_only(TenantUser.member_type),
                with_loader_criteria(
                    TenantUser, TenantUser.tenant_id == self.tenant_id
                ),
                selectinload(HospitalizationAction.hospitalization_action_attachments),
                selectinload(HospitalizationAction.sbar),
            )
        ).first()

    def paginate_by_hospitalization_id(
        self, hospitalization_id: UUID, page: int, limit: int
    ) -> Page[HospitalizationAction]:
        query = (
            select(HospitalizationAction)
            .where(
                HospitalizationAction.tenant_id == self.tenant_id,
                HospitalizationAction.hospitalization_id == hospitalization_id,
            )
            .order_by(HospitalizationAction.created_at.desc())
            .options(
                joinedload(HospitalizationAction.user),
                selectinload(HospitalizationAction.sbar),
            )
        )
        return paginate(
            self.session,
            query,
            Params(page=page, size=limit),
        )
