"""create hospitalization_actions table.

Revision ID: 1f08a0b4e0c3
Revises: ebba2271f598
Create Date: 2025-07-07 18:03:40.813713

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op
from app.enums.models.hospitalization_action_status_enums import (
    HospitalizationActionStatus,
)
from app.enums.models.hospitalization_action_type_enums import HospitalizationActionType

# revision identifiers, used by Alembic.
revision: str = "1f08a0b4e0c3"
down_revision: str | None = "ebba2271f598"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "hospitalization_actions",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("tenant_id", UUID(), nullable=False),
        sa.Column("hospitalization_id", UUID(), nullable=False),
        sa.Column("user_id", UUID(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                HospitalizationActionStatus, name="hospitalization_action_status_enum"
            ),
            nullable=False,
        ),
        sa.Column(
            "type",
            sa.Enum(HospitalizationActionType, name="hospitalization_action_type_enum"),
            nullable=False,
        ),
        sa.Column("description", sa.String(length=255), nullable=True),
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
        sa.ForeignKeyConstraint(["hospitalization_id"], ["hospitalizations.id"]),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("hospitalization_actions")
