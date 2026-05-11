"""create tenant_users table.

Revision ID: 7491d2e31caa
Revises: 5314882c1abc
Create Date: 2025-06-21 14:23:14.017162

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7491d2e31caa"
down_revision: str | None = "5314882c1abc"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tenant_users",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("tenant_id", UUID(), nullable=False),
        sa.Column("user_id", UUID(), nullable=False, index=True),
        sa.Column("role_id", UUID(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("tenant_id", "user_id", name="unique_tenant_user"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], name="fk_tenant_user"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_user_tenant"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], name="fk_role_tenant"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tenant_users")
