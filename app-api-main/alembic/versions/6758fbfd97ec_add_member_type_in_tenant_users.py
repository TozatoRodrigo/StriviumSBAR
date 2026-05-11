"""add member type in tenant users.

Revision ID: 6758fbfd97ec
Revises: 5caaae3bcd98
Create Date: 2025-12-11 13:52:44.436978

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
from app.enums.models.tenant_user_member_type_enums import TenantUserMemberType

# revision identifiers, used by Alembic.
revision: str = "6758fbfd97ec"
down_revision: str | None = "5caaae3bcd98"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    enum_type = sa.Enum(TenantUserMemberType, name="tenant_user_member_type_enum")
    enum_type.create(op.get_bind())
    op.add_column(
        "tenant_users",
        sa.Column(
            "member_type",
            enum_type,
            nullable=True,
            default=None,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("tenant_users", "member_type")
    sa.Enum(TenantUserMemberType, name="tenant_user_member_type_enum").drop(
        op.get_bind()
    )
