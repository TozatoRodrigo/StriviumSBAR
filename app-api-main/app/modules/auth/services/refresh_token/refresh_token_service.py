from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from app.models.refresh_token import RefreshToken
from app.modules.auth.exceptions.refresh_auth_error import RefreshAuthError
from app.modules.auth.repositories.refresh_token_repository import (
    RefreshTokenRepository,
)


class RefreshTokenService:
    def __init__(
        self, repository: RefreshTokenRepository, strict_mode: bool = True
    ) -> None:
        self.repository = repository
        self.strict_mode = strict_mode

    def create_token_record(
        self, user_id: UUID, token_type: str, expires_minutes: int
    ) -> tuple[UUID, UUID]:
        jti = uuid4()
        token_family = uuid4()
        expires_at = datetime.now(UTC) + timedelta(minutes=expires_minutes)

        record = RefreshToken(
            jti=jti,
            user_id=user_id,
            token_family=token_family,
            token_type=token_type,
            expires_at=expires_at,
        )
        self.repository.save(record)
        return jti, token_family

    def validate_and_rotate(
        self,
        jti: UUID | None,
        user_id: UUID,
        token_type: str,
        expires_minutes: int,
    ) -> tuple[UUID, UUID]:
        if jti is None:
            if self.strict_mode:
                raise RefreshAuthError
            return self.create_token_record(user_id, token_type, expires_minutes)

        token = self.repository.find_by_jti(jti)

        if token is None:
            if self.strict_mode:
                raise RefreshAuthError
            return self.create_token_record(user_id, token_type, expires_minutes)

        if token.user_id != user_id or token.token_type != token_type:
            self.repository.revoke_family(token.token_family)
            raise RefreshAuthError

        if token.revoked_at is not None:
            self.repository.revoke_family(token.token_family)
            raise RefreshAuthError

        token_expires_at = self._as_utc(token.expires_at)
        if token_expires_at <= datetime.now(UTC):
            self.repository.revoke(jti)
            raise RefreshAuthError

        self.repository.revoke(jti)

        new_jti = uuid4()
        expires_at = datetime.now(UTC) + timedelta(minutes=expires_minutes)

        record = RefreshToken(
            jti=new_jti,
            user_id=user_id,
            token_family=token.token_family,
            token_type=token_type,
            expires_at=expires_at,
        )
        self.repository.save(record)
        return new_jti, token.token_family

    def revoke_by_jti(self, jti: UUID) -> None:
        self.repository.revoke(jti)

    @staticmethod
    def _as_utc(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)
