"""increase description length in hospitalization action.

Revision ID: 5caaae3bcd98
Revises: 9a26f231abad
Create Date: 2025-10-26 21:29:42.935015

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5caaae3bcd98"
down_revision: str | None = "9a26f231abad"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("hospitalization_actions", "description", type_=sa.Text())


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "hospitalization_actions", "description", type_=sa.String(length=255)
    )
