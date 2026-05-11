from datetime import datetime, timedelta
from uuid import uuid4
from zoneinfo import ZoneInfo

from faker import Faker
from sqlmodel import Session

from app.core.database import engine
from app.enums.models.hospitalization_action_status_enums import (
    HospitalizationActionStatus,
)
from app.enums.models.hospitalization_action_type_enums import HospitalizationActionType
from app.models.hospitalization_action import HospitalizationAction
from app.modules.hospitalization.repositories.hospitalization_repository import (
    HospitalizationRepository,
)
from app.tests.hospitalization import create_hospitalization
from app.tests.patient import create_patient
from app.utils.timezone import set_timezone

fake = Faker()


class TestHospitalizationRepositoryPaginatePending:
    """Testes para paginate_pendings do HospitalizationRepository."""

    @staticmethod
    def test_paginate_pendings_should_return_hospitalizations_without_action_today() -> (
        None
    ):
        """Deve retornar internações sem ações criadas hoje."""
        with Session(engine) as session:
            timezone = ZoneInfo("America/Sao_Paulo")
            set_timezone(timezone)

            hospitalization = create_hospitalization()
            repository = HospitalizationRepository(session, hospitalization.tenant_id)

            yesterday = datetime.now(timezone) - timedelta(days=1)
            action = HospitalizationAction(
                tenant_id=hospitalization.tenant_id,
                hospitalization_id=hospitalization.id,
                status=HospitalizationActionStatus.COMPLETED,
                type=HospitalizationActionType.HOSPITALIZATION_VISIT,
                description=fake.sentence(),
                created_at=yesterday,
            )
            session.add(action)
            session.commit()

        result = repository.paginate_pendings(page=1, limit=10)

        assert result.total == 1
        assert result.items[0].id == hospitalization.id

    @staticmethod
    def test_paginate_pendings_should_not_return_hospitalizations_with_action_today() -> (
        None
    ):
        """Não deve retornar internações com ações criadas hoje."""
        with Session(engine) as session:
            timezone = ZoneInfo("America/Sao_Paulo")
            set_timezone(timezone)

            hospitalization = create_hospitalization()
            repository = HospitalizationRepository(session, hospitalization.tenant_id)

            today = datetime.now(timezone)
            action = HospitalizationAction(
                tenant_id=hospitalization.tenant_id,
                hospitalization_id=hospitalization.id,
                status=HospitalizationActionStatus.COMPLETED,
                type=HospitalizationActionType.HOSPITALIZATION_VISIT,
                description=fake.sentence(),
                created_at=today,
            )
            session.add(action)
            session.commit()

            result = repository.paginate_pendings(page=1, limit=10)

            assert result.total == 0

    @staticmethod
    def test_paginate_pendings_should_handle_action_before_midnight() -> None:
        """Deve tratar corretamente ação criada antes da meia-noite."""
        with Session(engine) as session:
            timezone = ZoneInfo("America/Sao_Paulo")
            set_timezone(timezone)

            hospitalization = create_hospitalization()
            repository = HospitalizationRepository(session, hospitalization.tenant_id)

            today = datetime.now(timezone).date()
            before_midnight = datetime.combine(today, datetime.min.time()) - timedelta(
                hours=1
            )
            before_midnight = before_midnight.replace(tzinfo=timezone)

            if datetime.now(timezone).hour == 0:
                before_midnight = datetime.now(timezone) - timedelta(hours=1)

            action = HospitalizationAction(
                tenant_id=hospitalization.tenant_id,
                hospitalization_id=hospitalization.id,
                status=HospitalizationActionStatus.COMPLETED,
                type=HospitalizationActionType.HOSPITALIZATION_VISIT,
                description=fake.sentence(),
                created_at=before_midnight,
            )
            session.add(action)
            session.commit()

        result = repository.paginate_pendings(page=1, limit=10)

        assert result.total == 1
        assert result.items[0].id == hospitalization.id

    @staticmethod
    def test_paginate_pendings_should_handle_action_at_midnight() -> None:
        """Deve tratar corretamente ação criada exatamente à meia-noite."""
        with Session(engine) as session:
            timezone = ZoneInfo("America/Sao_Paulo")
            set_timezone(timezone)

            hospitalization = create_hospitalization()
            repository = HospitalizationRepository(session, hospitalization.tenant_id)

            today = datetime.now(timezone).date()
            at_midnight = datetime.combine(today, datetime.min.time()).replace(
                tzinfo=timezone
            )

            action = HospitalizationAction(
                tenant_id=hospitalization.tenant_id,
                hospitalization_id=hospitalization.id,
                status=HospitalizationActionStatus.COMPLETED,
                type=HospitalizationActionType.HOSPITALIZATION_VISIT,
                description=fake.sentence(),
                created_at=at_midnight,
            )
            session.add(action)
            session.commit()

            result = repository.paginate_pendings(page=1, limit=10)

            assert result.total == 0

    @staticmethod
    def test_paginate_pendings_should_handle_action_one_hour_after_midnight() -> None:
        """Deve tratar corretamente ação criada 1 hora após a meia-noite."""
        with Session(engine) as session:
            timezone = ZoneInfo("America/Sao_Paulo")
            set_timezone(timezone)

            hospitalization = create_hospitalization()
            repository = HospitalizationRepository(session, hospitalization.tenant_id)

            today = datetime.now(timezone).date()
            one_hour_after_midnight = datetime.combine(
                today, datetime.min.time()
            ) + timedelta(hours=1)
            one_hour_after_midnight = one_hour_after_midnight.replace(tzinfo=timezone)

            action = HospitalizationAction(
                tenant_id=hospitalization.tenant_id,
                hospitalization_id=hospitalization.id,
                status=HospitalizationActionStatus.COMPLETED,
                type=HospitalizationActionType.HOSPITALIZATION_VISIT,
                description=fake.sentence(),
                created_at=one_hour_after_midnight,
            )
            session.add(action)
            session.commit()

            result = repository.paginate_pendings(page=1, limit=10)

            assert result.total == 0


class TestHospitalizationRepositoryPaginateCompleted:
    """Testes para paginate_completed do HospitalizationRepository."""

    @staticmethod
    def test_paginate_completed_should_return_hospitalizations_with_action_today() -> (
        None
    ):
        """Deve retornar internações com ações criadas hoje."""
        with Session(engine) as session:
            timezone = ZoneInfo("America/Sao_Paulo")
            set_timezone(timezone)

            hospitalization = create_hospitalization()
            repository = HospitalizationRepository(session, hospitalization.tenant_id)

            today = datetime.now(timezone)
            action = HospitalizationAction(
                tenant_id=hospitalization.tenant_id,
                hospitalization_id=hospitalization.id,
                status=HospitalizationActionStatus.COMPLETED,
                type=HospitalizationActionType.HOSPITALIZATION_VISIT,
                description=fake.sentence(),
                created_at=today,
            )
            session.add(action)
            session.commit()

        result = repository.paginate_completed(page=1, limit=10)

        assert result.total == 1
        assert result.items[0].id == hospitalization.id

    @staticmethod
    def test_paginate_completed_should_not_return_hospitalizations_without_action_today() -> (
        None
    ):
        """Não deve retornar internações sem ações criadas hoje."""
        with Session(engine) as session:
            timezone = ZoneInfo("America/Sao_Paulo")
            set_timezone(timezone)

            hospitalization = create_hospitalization()
            repository = HospitalizationRepository(session, hospitalization.tenant_id)

            yesterday = datetime.now(timezone) - timedelta(days=1)
            action = HospitalizationAction(
                tenant_id=hospitalization.tenant_id,
                hospitalization_id=hospitalization.id,
                status=HospitalizationActionStatus.COMPLETED,
                type=HospitalizationActionType.HOSPITALIZATION_VISIT,
                description=fake.sentence(),
                created_at=yesterday,
            )
            session.add(action)
            session.commit()

            result = repository.paginate_completed(page=1, limit=10)

            assert result.total == 0

    @staticmethod
    def test_paginate_completed_should_handle_action_before_midnight() -> None:
        """Deve tratar corretamente ação criada antes da meia-noite."""
        with Session(engine) as session:
            timezone = ZoneInfo("America/Sao_Paulo")
            set_timezone(timezone)

            hospitalization = create_hospitalization()
            repository = HospitalizationRepository(session, hospitalization.tenant_id)

            today = datetime.now(timezone).date()
            before_midnight = datetime.combine(today, datetime.min.time()) - timedelta(
                hours=1
            )
            before_midnight = before_midnight.replace(tzinfo=timezone)

            if datetime.now(timezone).hour == 0:
                before_midnight = datetime.now(timezone) - timedelta(hours=1)

            action = HospitalizationAction(
                tenant_id=hospitalization.tenant_id,
                hospitalization_id=hospitalization.id,
                status=HospitalizationActionStatus.COMPLETED,
                type=HospitalizationActionType.HOSPITALIZATION_VISIT,
                description=fake.sentence(),
                created_at=before_midnight,
            )
            session.add(action)
            session.commit()

            result = repository.paginate_completed(page=1, limit=10)

            assert result.total == 0

    @staticmethod
    def test_paginate_completed_should_handle_action_at_midnight() -> None:
        """Deve tratar corretamente ação criada exatamente à meia-noite."""
        with Session(engine) as session:
            timezone = ZoneInfo("America/Sao_Paulo")
            set_timezone(timezone)

            hospitalization = create_hospitalization()
            repository = HospitalizationRepository(session, hospitalization.tenant_id)

            today = datetime.now(timezone).date()
            at_midnight = datetime.combine(today, datetime.min.time()).replace(
                tzinfo=timezone
            )

            action = HospitalizationAction(
                tenant_id=hospitalization.tenant_id,
                hospitalization_id=hospitalization.id,
                status=HospitalizationActionStatus.COMPLETED,
                type=HospitalizationActionType.HOSPITALIZATION_VISIT,
                description=fake.sentence(),
                created_at=at_midnight,
            )
            session.add(action)
            session.commit()

        result = repository.paginate_completed(page=1, limit=10)

        assert result.total == 1
        assert result.items[0].id == hospitalization.id

    @staticmethod
    def test_paginate_completed_should_handle_action_one_hour_after_midnight() -> None:
        """Deve tratar corretamente ação criada 1 hora após a meia-noite."""
        with Session(engine) as session:
            timezone = ZoneInfo("America/Sao_Paulo")
            set_timezone(timezone)

            hospitalization = create_hospitalization()
            repository = HospitalizationRepository(session, hospitalization.tenant_id)

            today = datetime.now(timezone).date()
            one_hour_after_midnight = datetime.combine(
                today, datetime.min.time()
            ) + timedelta(hours=1)
            one_hour_after_midnight = one_hour_after_midnight.replace(tzinfo=timezone)

            action = HospitalizationAction(
                tenant_id=hospitalization.tenant_id,
                hospitalization_id=hospitalization.id,
                status=HospitalizationActionStatus.COMPLETED,
                type=HospitalizationActionType.HOSPITALIZATION_VISIT,
                description=fake.sentence(),
                created_at=one_hour_after_midnight,
            )
            session.add(action)
            session.commit()

        result = repository.paginate_completed(page=1, limit=10)

        assert result.total == 1
        assert result.items[0].id == hospitalization.id


class TestHospitalizationRepositoryPaginate:
    """Testes para paginate do HospitalizationRepository."""

    @staticmethod
    def test_paginate_should_return_all_hospitalizations_when_no_filter() -> None:
        """Deve retornar todas as internações quando nenhum filtro é aplicado."""
        with Session(engine) as session:
            hospitalization1 = create_hospitalization()
            hospitalization2 = create_hospitalization(
                {"tenant_id": hospitalization1.tenant_id}
            )
            repository = HospitalizationRepository(session, hospitalization1.tenant_id)

            result = repository.paginate(page=1, limit=10)

            assert result.total == 2  # noqa: PLR2004
            hospitalization_ids = [h.id for h in result.items]
            assert hospitalization1.id in hospitalization_ids
            assert hospitalization2.id in hospitalization_ids

    @staticmethod
    def test_paginate_should_return_hospitalizations_filtered_by_patient_id() -> None:
        """Deve retornar apenas internações do paciente especificado."""
        with Session(engine) as session:
            patient1 = create_patient()
            patient2 = create_patient({"tenant_id": patient1.tenant_id})
            hospitalization1 = create_hospitalization(
                {"tenant_id": patient1.tenant_id, "patient_id": patient1.id}
            )
            hospitalization2 = create_hospitalization(
                {"tenant_id": patient1.tenant_id, "patient_id": patient2.id}
            )
            hospitalization3 = create_hospitalization(
                {"tenant_id": patient1.tenant_id, "patient_id": patient1.id}
            )
            repository = HospitalizationRepository(session, patient1.tenant_id)

            result = repository.paginate(page=1, limit=10, patient_id=patient1.id)

            assert result.total == 2  # noqa: PLR2004
            hospitalization_ids = [h.id for h in result.items]
            assert hospitalization1.id in hospitalization_ids
            assert hospitalization3.id in hospitalization_ids
            assert hospitalization2.id not in hospitalization_ids

    @staticmethod
    def test_paginate_should_return_empty_when_patient_id_not_found() -> None:
        """Deve retornar vazio quando o patient_id não existe."""
        with Session(engine) as session:
            hospitalization = create_hospitalization()
            repository = HospitalizationRepository(session, hospitalization.tenant_id)
            fake_patient_id = uuid4()

            result = repository.paginate(page=1, limit=10, patient_id=fake_patient_id)

            assert result.total == 0
