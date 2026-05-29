"""add ai audit fields to hospitalization action sbars.

Revision ID: 3d2d8c5bb9f1
Revises: b1e7c4a9d6f2
Create Date: 2026-05-12 00:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3d2d8c5bb9f1"
down_revision: str | None = "b1e7c4a9d6f2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "hospitalization_action_sbars",
        sa.Column("plan", sa.Text(), nullable=True),
    )
    op.add_column(
        "hospitalization_action_sbars",
        sa.Column("source_transcript", sa.Text(), nullable=True),
    )
    op.add_column(
        "hospitalization_action_sbars",
        sa.Column(
            "ai_generated",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "hospitalization_action_sbars",
        sa.Column(
            "ai_review_confirmed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
    )
    op.add_column(
        "hospitalization_action_sbars",
        sa.Column("ai_warnings", sa.JSON(), nullable=True),
    )
    op.add_column(
        "hospitalization_action_sbars",
        sa.Column("ai_missing_information", sa.JSON(), nullable=True),
    )
    op.add_column(
        "hospitalization_action_sbars",
        sa.Column("ai_confidence", sa.JSON(), nullable=True),
    )
    op.alter_column("hospitalization_action_sbars", "ai_generated", server_default=None)
    op.alter_column(
        "hospitalization_action_sbars", "ai_review_confirmed", server_default=None
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("hospitalization_action_sbars", "ai_confidence")
    op.drop_column("hospitalization_action_sbars", "ai_missing_information")
    op.drop_column("hospitalization_action_sbars", "ai_warnings")
    op.drop_column("hospitalization_action_sbars", "ai_review_confirmed")
    op.drop_column("hospitalization_action_sbars", "ai_generated")
    op.drop_column("hospitalization_action_sbars", "source_transcript")
    op.drop_column("hospitalization_action_sbars", "plan")
