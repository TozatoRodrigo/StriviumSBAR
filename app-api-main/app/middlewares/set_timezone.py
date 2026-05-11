from zoneinfo import ZoneInfo

from starlette.datastructures import Headers
from starlette.types import ASGIApp, Receive, Scope, Send

from app.utils.timezone import set_timezone


class SetTimezoneMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        headers = Headers(scope=scope)
        timezone = headers.get("X-Timezone", "UTC")
        try:
            timezone = ZoneInfo(timezone)
        except Exception:
            timezone = ZoneInfo("UTC")
        set_timezone(timezone)
        await self.app(scope, receive, send)
