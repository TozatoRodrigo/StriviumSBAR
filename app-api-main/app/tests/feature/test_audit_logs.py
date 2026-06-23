"""Tests for the audit logging system (LGPD Art. 46/48)."""

from datetime import datetime, timedelta

from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.database import engine
from app.enums.models.audit_enums import AuditAction, AuditResource
from app.main import app as production_app
from app.middlewares.audit_middleware import AuditLogMiddleware, _match
from app.models.audit_log import AuditLog
from app.modules.audit.repositories.audit_log_repository import AuditLogRepository
from app.scripts.purge_audit_logs import purge_audit_logs
from app.services.audit.audit_log_service import AuditLogService
from app.tests.tenant import (
    create_role_without_permissions,
    create_tenant,
    create_tenant_access_token,
    create_tenant_user,
)
from app.tests.user import create_user

SAMPLE_UUID = "123e4567-e89b-12d3-a456-426614174000"


def _count_logs(action: str | None = None) -> int:
    with Session(engine) as session:
        query = select(AuditLog)
        if action is not None:
            query = query.where(AuditLog.action == action)
        return len(session.exec(query).all())


# --- route matching ---------------------------------------------------------


def test_match_identifies_sensitive_routes() -> None:
    matched = _match("GET", f"/patient/v1/patients/{SAMPLE_UUID}")
    assert matched is not None
    route, match = matched
    assert route.action == AuditAction.VIEW_PATIENT.value
    assert match.groupdict()["id"] == SAMPLE_UUID


def test_match_ignores_non_sensitive_routes() -> None:
    assert _match("GET", "/health") is None
    assert _match("GET", "/patient/v1/patients") is None


# --- service + repository ---------------------------------------------------


def test_service_records_audit_entry() -> None:
    with Session(engine) as session:
        service = AuditLogService(AuditLogRepository(session))
        entry = service.record(
            action=AuditAction.VIEW_PATIENT.value,
            resource_type=AuditResource.PATIENT.value,
            resource_id=SAMPLE_UUID,
            ip_address="10.0.0.1",
        )
    assert entry.id is not None
    assert _count_logs(AuditAction.VIEW_PATIENT.value) == 1


def test_repository_paginates_and_filters() -> None:
    with Session(engine) as session:
        repository = AuditLogRepository(session)
        repository.save(AuditLog(action=AuditAction.LOGIN.value))
        repository.save(AuditLog(action=AuditAction.VIEW_PATIENT.value))

        page = repository.paginate(1, 10, action=AuditAction.LOGIN.value)

    assert page.total == 1
    assert page.items[0].action == AuditAction.LOGIN.value


def test_repository_delete_older_than_purges() -> None:
    with Session(engine) as session:
        repository = AuditLogRepository(session)
        repository.save(
            AuditLog(
                action=AuditAction.LOGIN.value,
                created_at=datetime.now() - timedelta(days=400),
            )
        )
        repository.save(AuditLog(action=AuditAction.LOGIN.value))

        deleted = repository.delete_older_than(datetime.now() - timedelta(days=180))

    assert deleted == 1
    assert _count_logs() == 1


def test_purge_script_respects_retention() -> None:
    with Session(engine) as session:
        AuditLogRepository(session).save(
            AuditLog(
                action=AuditAction.LOGIN.value,
                created_at=datetime.now() - timedelta(days=400),
            )
        )
    deleted = purge_audit_logs()
    assert deleted >= 1


# --- middleware integration -------------------------------------------------


def _build_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(AuditLogMiddleware)

    @app.get("/patient/v1/patients/{patient_id}")
    async def view_patient(patient_id: str) -> dict[str, str]:
        return {"id": patient_id}

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


def test_middleware_records_sensitive_request() -> None:
    client = TestClient(_build_app())

    response = client.get(f"/patient/v1/patients/{SAMPLE_UUID}")

    assert response.status_code == status.HTTP_200_OK
    with Session(engine) as session:
        entries = session.exec(
            select(AuditLog).where(AuditLog.action == AuditAction.VIEW_PATIENT.value)
        ).all()
    assert len(entries) == 1
    assert entries[0].resource_id == SAMPLE_UUID
    assert entries[0].resource_type == AuditResource.PATIENT.value
    assert entries[0].status_code == status.HTTP_200_OK


def test_middleware_skips_non_sensitive_request() -> None:
    client = TestClient(_build_app())

    client.get("/health")

    assert _count_logs() == 0


# --- admin endpoint ---------------------------------------------------------


def test_audit_logs_endpoint_requires_authentication() -> None:
    client = TestClient(production_app)
    response = client.get("/audit/v1/logs")
    assert response.status_code in {
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    }


def test_audit_logs_endpoint_returns_paginated_logs() -> None:
    tenant = create_tenant()
    token = create_tenant_access_token({"tenant_id": tenant.id})
    with Session(engine) as session:
        AuditLogRepository(session).save(AuditLog(action=AuditAction.LOGIN.value))

    client = TestClient(production_app)
    response = client.get(
        "/audit/v1/logs",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["total"] >= 1
    assert isinstance(body["data"], list)


def test_audit_logs_endpoint_forbidden_without_permission() -> None:
    tenant = create_tenant()
    user = create_user()
    role = create_role_without_permissions()
    create_tenant_user({"user_id": user.id, "tenant_id": tenant.id, "role_id": role.id})
    token = create_tenant_access_token({"tenant_id": tenant.id, "user_id": user.id})

    client = TestClient(production_app)
    response = client.get(
        "/audit/v1/logs",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
