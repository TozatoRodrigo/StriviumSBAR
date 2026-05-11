"""create hospitalization action sbars table.

Revision ID: b1e7c4a9d6f2
Revises: 7192598ff635
Create Date: 2026-05-11 15:05:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op
from app.enums.models.hospitalization_action_sbar_clinical_course_enums import (
    HospitalizationActionSbarClinicalCourse,
)
from app.enums.models.hospitalization_action_sbar_priority_enums import (
    HospitalizationActionSbarPriority,
)

# revision identifiers, used by Alembic.
revision: str = "b1e7c4a9d6f2"
down_revision: str | None = "7192598ff635"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    priority_enum = sa.Enum(
        HospitalizationActionSbarPriority,
        name="hospitalization_action_sbar_priority_enum",
    )
    clinical_course_enum = sa.Enum(
        HospitalizationActionSbarClinicalCourse,
        name="hospitalization_action_sbar_clinical_course_enum",
    )
    op.create_table(
        "hospitalization_action_sbars",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("tenant_id", UUID(), nullable=False),
        sa.Column("hospitalization_action_id", UUID(), nullable=False),
        sa.Column("situation", sa.Text(), nullable=False),
        sa.Column("background", sa.Text(), nullable=True),
        sa.Column("assessment", sa.Text(), nullable=False),
        sa.Column("recommendation", sa.Text(), nullable=False),
        sa.Column("priority", priority_enum, nullable=False),
        sa.Column("clinical_course", clinical_course_enum, nullable=True),
        sa.Column("pending_items", sa.Text(), nullable=True),
        sa.Column("alerts", sa.Text(), nullable=True),
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
        sa.ForeignKeyConstraint(
            ["hospitalization_action_id"], ["hospitalization_actions.id"]
        ),
        sa.UniqueConstraint("hospitalization_action_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("hospitalization_action_sbars")
    sa.Enum(
        HospitalizationActionSbarClinicalCourse,
        name="hospitalization_action_sbar_clinical_course_enum",
    ).drop(op.get_bind())
    sa.Enum(
        HospitalizationActionSbarPriority,
        name="hospitalization_action_sbar_priority_enum",
    ).drop(op.get_bind())
