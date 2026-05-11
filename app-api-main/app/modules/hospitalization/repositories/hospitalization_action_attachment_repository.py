from sqlmodel import Session

from app.models.hospitalization_action_attachment import HospitalizationActionAttachment


class HospitalizationActionAttachmentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(
        self, hospitalization_action_attachment: HospitalizationActionAttachment
    ) -> HospitalizationActionAttachment:
        self.session.add(hospitalization_action_attachment)
        self.session.commit()
        self.session.refresh(hospitalization_action_attachment)
        return hospitalization_action_attachment
