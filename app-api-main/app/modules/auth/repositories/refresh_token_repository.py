from datetime import UTC, datetime
from uuid import UUID

from sqlmodel import Session, select

from app.models.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, refresh_token: RefreshToken) -> RefreshToken:
        self.session.add(refresh_token)
        self.session.commit()
        self.session.refresh(refresh_token)
        return refresh_token

    def find_by_jti(self, jti: UUID) -> RefreshToken | None:
        return self.session.exec(
            select(RefreshToken).where(RefreshToken.jti == jti)
        ).first()

    def revoke(self, jti: UUID) -> None:
        token = self.find_by_jti(jti)
        if token and token.revoked_at is None:
            token.revoked_at = datetime.now(UTC)
            self.session.add(token)
            self.session.commit()

    def revoke_family(self, token_family: UUID) -> None:
        tokens = self.session.exec(
            select(RefreshToken).where(
                RefreshToken.token_family == token_family,
                RefreshToken.revoked_at.is_(None),
            )
        ).all()
        now = datetime.now(UTC)
        for token in tokens:
            token.revoked_at = now
            self.session.add(token)
        self.session.commit()

    def is_revoked(self, jti: UUID) -> bool:
        token = self.find_by_jti(jti)
        if token is None:
            return True
        return token.revoked_at is not None
