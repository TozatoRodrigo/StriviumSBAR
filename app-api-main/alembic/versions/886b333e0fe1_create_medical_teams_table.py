"""create medical_teams table.

Revision ID: 886b333e0fe1
Revises: 7491d2e31caa
Create Date: 2025-06-28 16:08:26.706530

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
from app.enums.models.medical_teams_enums import MedicalTeamStatus

# revision identifiers, used by Alembic.
revision: str = "886b333e0fe1"
down_revision: str | None = "7491d2e31caa"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "medical_teams",
        sa.Column(
            "id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column(
            "tenant_id",
            sa.UUID(),
            nullable=False,
            index=True,
        ),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column(
            "status",
            sa.Enum(MedicalTeamStatus, name="medical_team_status_enum"),
            nullable=False,
            default=MedicalTeamStatus.ACTIVE,
        ),
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
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"]),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("medical_teams")
