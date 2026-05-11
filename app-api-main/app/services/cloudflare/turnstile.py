from typing import Any

import httpx


class TurnstileService:
    @staticmethod
    async def validate(
        token: str, secret: str, remoteip: str | None = None
    ) -> dict[str, Any]:
        url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"

        data = {"secret": secret, "response": token}

        if remoteip:
            data["remoteip"] = remoteip

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data, timeout=10)
                response.raise_for_status()
                return response.json()
        except Exception:
            return {"success": False, "error-codes": ["internal-error"]}
