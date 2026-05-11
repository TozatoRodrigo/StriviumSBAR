from jose import JWTError, jwt

from app.core.environment import envs


def verify(token: str) -> bool:
    try:
        payload = jwt.decode(token, envs.JWT_SECRET, algorithms=["HS256"])
        return bool(payload)
    except JWTError:
        return False


def decode(token: str) -> dict:
    return jwt.decode(token, envs.JWT_SECRET, algorithms=["HS256"])
