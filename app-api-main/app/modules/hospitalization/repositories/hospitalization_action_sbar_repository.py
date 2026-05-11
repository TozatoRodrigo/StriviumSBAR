from uuid import UUID

from sqlmodel import Session, select

from app.models.hospitalization_action_sbar import HospitalizationActionSbar


class HospitalizationActionSbarRepository:
    def __init__(self, session: Session, tenant_id: UUID) -> None:
        self.session = session
        self.tenant_id = tenant_id

    def upsert(self, sbar: HospitalizationActionSbar) -> HospitalizationActionSbar:
        existing_sbar = self.find_by_hospitalization_action_id(
            sbar.hospitalization_action_id
        )
        if existing_sbar:
            existing_sbar.situation = sbar.situation
            existing_sbar.background = sbar.background
            existing_sbar.assessment = sbar.assessment
            existing_sbar.recommendation = sbar.recommendation
            existing_sbar.priority = sbar.priority
            existing_sbar.clinical_course = sbar.clinical_course
            existing_sbar.pending_items = sbar.pending_items
            existing_sbar.alerts = sbar.alerts
            sbar = existing_sbar

        self.session.add(sbar)
        self.session.commit()
        self.session.refresh(sbar)
        return sbar

    def find_by_hospitalization_action_id(
        self, hospitalization_action_id: UUID
    ) -> HospitalizationActionSbar | None:
        return self.session.exec(
            select(HospitalizationActionSbar).where(
                HospitalizationActionSbar.hospitalization_action_id
                == hospitalization_action_id,
                HospitalizationActionSbar.tenant_id == self.tenant_id,
            )
        ).first()
