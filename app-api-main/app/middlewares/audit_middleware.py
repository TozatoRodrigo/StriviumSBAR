"""Audit logging middleware (LGPD Art. 46/48).

Records an audit trail entry for sensitive HTTP routes: who (user/tenant from
the JWT), what (action/resource derived from method + path), when, from where
(IP, user-agent) and the resulting status. Recording happens after the response
is produced and never blocks or breaks the request (failures are swallowed).

The set of audited routes is declared in ``_AUDITED_ROUTES`` and is easy to
extend. To respect data minimization, only access metadata is stored here;
field-level before/after diffs are recorded by use cases that call
``AuditLogService.record`` with a ``changes`` payload.
"""

import re
from dataclasses import dataclass
from uuid import UUID

from jose import jwt
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.environment import envs
from app.enums.models.audit_enums import AuditAction, AuditResource
from app.services.audit.audit_log_service import record_audit_event

HTTP_ERROR_THRESHOLD = 400
_UUID_RE = r"[0-9a-fA-F-]{36}"


@dataclass(frozen=True)
class _AuditRoute:
    method: str
    pattern: re.Pattern[str]
    action: str
    resource_type: str
    failure_action: str | None = None


def _route(
    method: str,
    regex: str,
    action: AuditAction,
    resource: AuditResource,
    failure: AuditAction | None = None,
) -> _AuditRoute:
    return _AuditRoute(
        method=method,
        pattern=re.compile(regex),
        action=action.value,
        resource_type=resource.value,
        failure_action=failure.value if failure else None,
    )


# Sensitive routes to audit (see the story's "Dados a Auditar").
_AUDITED_ROUTES: list[_AuditRoute] = [
    _route(
        "POST",
        r"^/auth/v1/login/?$",
        AuditAction.LOGIN,
        AuditResource.AUTH,
        AuditAction.LOGIN_FAILED,
    ),
    _route("POST", r"^/auth/v1/logout/?$", AuditAction.LOGOUT, AuditResource.AUTH),
    _route(
        "POST",
        r"^/patient/v1/patients/?$",
        AuditAction.CREATE_PATIENT,
        AuditResource.PATIENT,
    ),
    _route(
        "GET",
        rf"^/patient/v1/patients/(?P<id>{_UUID_RE})/?$",
        AuditAction.VIEW_PATIENT,
        AuditResource.PATIENT,
    ),
    _route(
        "PUT",
        rf"^/patient/v1/patients/(?P<id>{_UUID_RE})/?$",
        AuditAction.UPDATE_PATIENT,
        AuditResource.PATIENT,
    ),
    _route(
        "POST",
        r"^/hospitalization/v1/hospitalizations/?$",
        AuditAction.CREATE_HOSPITALIZATION,
        AuditResource.HOSPITALIZATION,
    ),
    _route(
        "GET",
        rf"^/hospitalization/v1/hospitalizations/(?P<id>{_UUID_RE})/?$",
        AuditAction.VIEW_HOSPITALIZATION,
        AuditResource.HOSPITALIZATION,
    ),
    _route(
        "PUT",
        rf"^/hospitalization/v1/hospitalizations/(?P<id>{_UUID_RE})/?$",
        AuditAction.UPDATE_HOSPITALIZATION,
        AuditResource.HOSPITALIZATION,
    ),
    _route(
        "POST",
        rf"^/hospitalization/v1/hospitalizations/(?P<id>{_UUID_RE})"
        r"/hospitalization-actions/?$",
        AuditAction.CREATE_HOSPITALIZATION_ACTION,
        AuditResource.HOSPITALIZATION_ACTION,
    ),
    _route(
        "POST", r"^/api/sbar/extract/?$", AuditAction.CREATE_SBAR, AuditResource.SBAR
    ),
    _route(
        "POST",
        r"^/tenant-user/v1/tenant-users/?$",
        AuditAction.CREATE_TENANT_USER,
        AuditResource.TENANT_USER,
    ),
]


def _to_uuid(value: object) -> UUID | None:
    try:
        return UUID(str(value))
    except (ValueError, TypeError):
        return None


def _match(method: str, path: str) -> tuple[_AuditRoute, re.Match[str]] | None:
    for route in _AUDITED_ROUTES:
        if route.method != method:
            continue
        match = route.pattern.match(path)
        if match:
            return route, match
    return None


def _identity_from_token(authorization: str | None) -> tuple[UUID | None, UUID | None]:
    """Resolve the caller identity from the bearer token; never raises.

    Returns:
        A ``(user_id, tenant_id)`` tuple, with ``None`` for values that cannot
        be determined (missing/invalid token or unknown token type).

    """
    if not authorization or not authorization.startswith("Bearer "):
        return None, None

    token = authorization.removeprefix("Bearer ").strip()
    try:
        payload = jwt.decode(token, envs.JWT_SECRET, algorithms=["HS256"])
    except Exception:
        return None, None

    claim_type = payload.get("type")
    if claim_type == "tenant":
        user = payload.get("user") or {}
        return _to_uuid(user.get("id")), _to_uuid(payload.get("sub"))
    if claim_type == "user":
        return _to_uuid(payload.get("sub")), None
    return None, None


def _client_ip(scope: Scope, headers: Headers) -> str | None:
    forwarded = headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    client = scope.get("client")
    return client[0] if client else None


class AuditLogMiddleware:
    """Record audit entries for the configured sensitive routes."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or not envs.AUDIT_LOG_ENABLED:
            await self.app(scope, receive, send)
            return

        matched = _match(scope["method"], scope.get("path", ""))
        if matched is None:
            await self.app(scope, receive, send)
            return

        route, match = matched
        status_code = 0

        async def send_wrapper(message: Message) -> None:
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message["status"]
            await send(message)

        await self.app(scope, receive, send_wrapper)

        headers = Headers(scope=scope)
        user_id, tenant_id = _identity_from_token(headers.get("authorization"))
        action = route.action
        if route.failure_action and status_code >= HTTP_ERROR_THRESHOLD:
            action = route.failure_action

        record_audit_event(
            action=action,
            user_id=user_id,
            tenant_id=tenant_id,
            resource_type=route.resource_type,
            resource_id=match.groupdict().get("id"),
            method=scope["method"],
            path=scope.get("path"),
            status_code=status_code,
            ip_address=_client_ip(scope, headers),
            user_agent=headers.get("user-agent"),
        )
