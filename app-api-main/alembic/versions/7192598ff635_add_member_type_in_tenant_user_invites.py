"""add member type in tenant user invites.

Revision ID: 7192598ff635
Revises: 6758fbfd97ec
Create Date: 2025-12-11 13:52:54.805790

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
from app.enums.models.tenant_user_invite_member_type_enums import (
    TenantUserInviteMemberType,
)

# revision identifiers, used by Alembic.
revision: str = "7192598ff635"
down_revision: str | None = "6758fbfd97ec"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    enum_type = sa.Enum(
        TenantUserInviteMemberType, name="tenant_user_invite_member_type_enum"
    )
    enum_type.create(op.get_bind())
    op.add_column(
        "tenant_user_invites",
        sa.Column(
            "member_type",
            enum_type,
            nullable=True,
            default=None,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("tenant_user_invites", "member_type")
    sa.Enum(
        TenantUserInviteMemberType, name="tenant_user_invite_member_type_enum"
    ).drop(op.get_bind())
