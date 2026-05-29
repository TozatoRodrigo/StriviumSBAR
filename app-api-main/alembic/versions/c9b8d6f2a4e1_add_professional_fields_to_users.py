"""add professional fields to users.

Revision ID: c9b8d6f2a4e1
Revises: 3d2d8c5bb9f1
Create Date: 2026-05-13 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c9b8d6f2a4e1"
down_revision: str | None = "3d2d8c5bb9f1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("cellphone", sa.String(length=20), nullable=True))
    op.add_column("users", sa.Column("gender", sa.String(length=20), nullable=True))
    op.add_column("users", sa.Column("specialty", sa.String(length=100), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "specialty")
    op.drop_column("users", "gender")
    op.drop_column("users", "cellphone")
