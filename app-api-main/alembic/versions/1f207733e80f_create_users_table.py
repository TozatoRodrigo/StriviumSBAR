"""create users table.

Revision ID: 1f207733e80f
Revises: 12eeabdc9f11
Create Date: 2025-06-13 17:44:40.063114

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1f207733e80f"
down_revision: str | None = "12eeabdc9f11"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("first_name", sa.String(length=150), nullable=False),
        sa.Column("last_name", sa.String(length=150), nullable=False),
        sa.Column("document", sa.String(length=11), nullable=True, unique=True),
        sa.Column("crm_state", sa.String(length=2), nullable=True),
        sa.Column("crm_number", sa.String(length=50), nullable=True),
        sa.Column(
            "email", sa.String(length=150), nullable=False, unique=True, index=True
        ),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=False),
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
        sa.UniqueConstraint(
            "crm_state", "crm_number", name="unique_users_crm_state_crm_number"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
