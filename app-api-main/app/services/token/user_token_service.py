from jose import jwt

from app.core.environment import envs
from app.modules.user.exceptions.user_not_found_error import UserNotFoundError


class UserTokenService:
    def __init__(self, token: str) -> None:
        self.token = token.replace("Bearer ", "")

    def get_user_id_from_token(self) -> str:
        if not self.token:
            msg = "Não foi possível obter o usuario autenticado"
            raise UserNotFoundError(msg)

        try:
            payload = jwt.decode(self.token, envs.JWT_SECRET, algorithms=["HS256"])
            return payload["sub"]
        except Exception as e:
            msg = "Não foi possível obter o usuario autenticado"
            raise UserNotFoundError(msg) from e

    def get_user_id_from_tenant_token(self) -> str:
        if not self.token:
            msg = "Não foi possível obter o usuario autenticado"
            raise UserNotFoundError(msg)

        try:
            payload = jwt.decode(self.token, envs.JWT_SECRET, algorithms=["HS256"])
            return payload["user"]["id"]
        except Exception as e:
            msg = "Não foi possível obter o usuario autenticado"
            raise UserNotFoundError(msg) from e

    def get_tenant_id_from_token(self) -> str:
        if not self.token:
            msg = "Não foi possível obter o usuario autenticado"
            raise UserNotFoundError(msg)

        try:
            payload = jwt.decode(self.token, envs.JWT_SECRET, algorithms=["HS256"])
            return payload["sub"]
        except Exception as e:
            msg = "Não foi possível obter o usuario autenticado"
            raise UserNotFoundError(msg) from e
