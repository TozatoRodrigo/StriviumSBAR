"""create role_permissions table.

Revision ID: 5314882c1abc
Revises: ed75292ba557
Create Date: 2025-06-21 14:23:06.496370

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5314882c1abc"
down_revision: str | None = "ed75292ba557"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "role_permissions",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("role_id", UUID(), nullable=False),
        sa.Column("permission_id", UUID(), nullable=False),
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
        sa.UniqueConstraint("role_id", "permission_id", name="unique_role_permission"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], name="fk_role_permission"),
        sa.ForeignKeyConstraint(
            ["permission_id"],
            ["permissions.id"],
            name="fk_permission_role",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("role_permissions")
