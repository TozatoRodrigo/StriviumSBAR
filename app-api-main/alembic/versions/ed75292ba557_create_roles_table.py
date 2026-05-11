"""create roles table.

Revision ID: ed75292ba557
Revises: a765384729ff
Create Date: 2025-06-21 14:22:59.870496

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "ed75292ba557"
down_revision: str | None = "a765384729ff"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "roles",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("name", sa.String(length=150), nullable=False, unique=True),
        sa.Column("description", sa.String(length=150), nullable=False),
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
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("roles")
