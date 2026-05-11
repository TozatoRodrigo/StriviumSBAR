"""create hospitalizations table.

Revision ID: ebba2271f598
Revises: 248c675bb053
Create Date: 2025-07-07 17:53:01.520290

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op
from app.enums.models.hospitalization_status_enums import HospitalizationStatus

# revision identifiers, used by Alembic.
revision: str = "ebba2271f598"
down_revision: str | None = "248c675bb053"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "hospitalizations",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("tenant_id", UUID(), nullable=False),
        sa.Column("user_id", UUID(), nullable=False),
        sa.Column("patient_id", UUID(), nullable=False),
        sa.Column("medical_team_id", UUID(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(HospitalizationStatus, name="hospitalization_status_enum"),
            nullable=False,
            default=HospitalizationStatus.ACTIVE,
        ),
        sa.Column("hospitalization_number", sa.String(length=50), nullable=True),
        sa.Column("hospitalization_place", sa.String(length=100), nullable=True),
        sa.Column("hospitalization_sector", sa.String(length=100), nullable=True),
        sa.Column("hospitalization_reason", sa.String(length=150), nullable=True),
        sa.Column("observation", sa.String(length=255), nullable=True),
        sa.Column(
            "discharged_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True,
            default=None,
        ),
        sa.Column(
            "deceased_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True,
            default=None,
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
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"]),
        sa.ForeignKeyConstraint(["medical_team_id"], ["medical_teams.id"]),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("hospitalizations")
