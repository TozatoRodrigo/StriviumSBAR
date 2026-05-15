from jose import jwt

from app.core.environment import envs
from app.exceptions.authentication_error import AuthenticationError


class UserTokenService:
    def __init__(self, token: str) -> None:
        self.token = token.replace("Bearer ", "")

    def get_user_id_from_token(self) -> str:
        if not self.token or not self.token.strip():
            raise AuthenticationError

        try:
            payload = jwt.decode(self.token, envs.JWT_SECRET, algorithms=["HS256"])
            if payload.get("type") != "user":
                raise AuthenticationError
            return payload["sub"]
        except AuthenticationError:
            raise
        except Exception as e:
            raise AuthenticationError from e

    def get_user_id_from_tenant_token(self) -> str:
        if not self.token or not self.token.strip():
            raise AuthenticationError

        try:
            payload = jwt.decode(self.token, envs.JWT_SECRET, algorithms=["HS256"])
            if payload.get("type") != "tenant":
                raise AuthenticationError
            return payload["user"]["id"]
        except AuthenticationError:
            raise
        except Exception as e:
            raise AuthenticationError from e

    def get_tenant_id_from_token(self) -> str:
        if not self.token or not self.token.strip():
            raise AuthenticationError

        try:
            payload = jwt.decode(self.token, envs.JWT_SECRET, algorithms=["HS256"])
            if payload.get("type") != "tenant":
                raise AuthenticationError
            return payload["sub"]
        except AuthenticationError:
            raise
        except Exception as e:
            raise AuthenticationError from e
