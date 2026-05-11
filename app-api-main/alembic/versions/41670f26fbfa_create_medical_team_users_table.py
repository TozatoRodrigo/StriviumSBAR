"""create medical_team_users table.

Revision ID: 41670f26fbfa
Revises: 886b333e0fe1
Create Date: 2025-06-28 16:08:31.260569

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
from app.enums.models.medical_team_users_enums import MedicalTeamUserStatus

# revision identifiers, used by Alembic.
revision: str = "41670f26fbfa"
down_revision: str | None = "886b333e0fe1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "medical_team_users",
        sa.Column(
            "id", sa.UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column(
            "tenant_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "medical_team_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.UUID(),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum(MedicalTeamUserStatus, name="medical_team_user_status_enum"),
            nullable=False,
            default=MedicalTeamUserStatus.ACTIVE,
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
        sa.ForeignKeyConstraint(["medical_team_id"], ["medical_teams.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.UniqueConstraint(
            "tenant_id",
            "medical_team_id",
            "user_id",
        ),
        sa.Index(
            "ix_medical_team_users_tenant_id_medical_team_id_user_id",
            "tenant_id",
            "medical_team_id",
            "user_id",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("medical_team_users")
