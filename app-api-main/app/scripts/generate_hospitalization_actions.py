from datetime import datetime, time

from sqlmodel import not_, select

from app.core.database import get_session
from app.core.logging import logger
from app.enums.models.hospitalization_action_status_enums import (
    HospitalizationActionStatus,
)
from app.enums.models.hospitalization_action_type_enums import HospitalizationActionType
from app.enums.models.hospitalization_status_enums import HospitalizationStatus
from app.models.hospitalization import Hospitalization
from app.models.hospitalization_action import HospitalizationAction

session = next(get_session())


def get_hospitalizations_to_generate_action() -> list[Hospitalization]:
    query = select(Hospitalization).where(
        Hospitalization.status == HospitalizationStatus.ACTIVE,
        not_(
            select(HospitalizationAction.id)
            .where(
                HospitalizationAction.hospitalization_id == Hospitalization.id,
                HospitalizationAction.created_at
                >= datetime.combine(datetime.now().date(), time.min),
                HospitalizationAction.created_at
                <= datetime.combine(datetime.now().date(), time.max),
            )
            .exists()
        ),
    )
    return session.exec(query).all()


def generate_new_hospitalization_actions() -> None:
    logger.info("generating new hospitalization actions")
    hospitalizations = get_hospitalizations_to_generate_action()
    for hospitalization in hospitalizations:
        logger.info(
            f"generating new hospitalization action for hospitalization {hospitalization.id}"
        )
        action = HospitalizationAction(
            tenant_id=hospitalization.tenant_id,
            hospitalization_id=hospitalization.id,
            user_id=hospitalization.user_id,
            status=HospitalizationActionStatus.PENDING,
            type=HospitalizationActionType.HOSPITALIZATION_VISIT,
            description="",
        )
        session.add(action)
        session.commit()
        logger.info(
            f"new hospitalization action for hospitalization {hospitalization.id} generated"
        )


def get_actions_to_cancel() -> list[HospitalizationAction]:
    query = select(HospitalizationAction).where(
        HospitalizationAction.status == HospitalizationActionStatus.PENDING,
        HospitalizationAction.created_at
        < datetime.combine(datetime.now().date(), time.min),
    )
    return session.exec(query).all()


def cancel_actions() -> None:
    logger.info("cancelling actions")
    actions_to_cancel = get_actions_to_cancel()
    for action in actions_to_cancel:
        logger.info(f"cancelling action {action.id}")
        action.status = HospitalizationActionStatus.SKIPPED
        session.add(action)
        session.commit()
        logger.info(f"action {action.id} cancelled")


logger.info("running daily hospitalization actions")
if __name__ == "__main__":
    cancel_actions()
    generate_new_hospitalization_actions()
    session.close()
