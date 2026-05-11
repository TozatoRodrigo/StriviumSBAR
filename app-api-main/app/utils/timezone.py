from contextvars import ContextVar
from zoneinfo import ZoneInfo

timezone_default = ZoneInfo("UTC")
request_timezone: ContextVar[ZoneInfo] = ContextVar(
    "request_timezone", default=timezone_default
)


def set_timezone(timezone: ZoneInfo) -> None:
    request_timezone.set(timezone)


def get_timezone() -> ZoneInfo:
    return request_timezone.get()
