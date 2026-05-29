from faker import Faker

from app.core.database import get_session
from app.models.user import User
from app.modules.auth.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)
from app.modules.auth.services.refresh_token.refresh_token_service import (
    RefreshTokenService,
)
from app.modules.auth.utils.jwt import (
    REFRESH_TOKEN_EXPIRES_MINUTES,
    generate_access_token,
    generate_refresh_token,
)
from app.modules.user.utils.bcrypt import hash_password

fake = Faker()


def create_user() -> User:
    user = User(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        crm_state=None,
        crm_number=None,
        document=None,
        password=hash_password(fake.password()),
        birth_date=fake.date_of_birth(minimum_age=18, maximum_age=100),
    )
    session = next(get_session())
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()
    return user


def create_access_token(user: User | None = None) -> str:
    if user is None:
        user = create_user()
    payload = {
        "sub": str(user.id),
        "type": "user",
        "user": {
            "id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        },
    }
    return generate_access_token(payload)


def create_refresh_token(user: User | None = None) -> str:
    if user is None:
        user = create_user()

    session = next(get_session())
    refresh_token_repository = RefreshTokenRepository(session)
    refresh_token_service = RefreshTokenService(refresh_token_repository)
    jti, _token_family = refresh_token_service.create_token_record(
        user_id=user.id,
        token_type="user-refresh",  # noqa: S106
        expires_minutes=REFRESH_TOKEN_EXPIRES_MINUTES,
    )
    session.close()

    payload = {
        "sub": str(user.id),
        "type": "user-refresh",
    }
    return generate_refresh_token(payload, jti=jti)
