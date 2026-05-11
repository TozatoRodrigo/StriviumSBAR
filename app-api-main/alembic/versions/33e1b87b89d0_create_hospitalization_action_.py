"""create hospitalization_action_attachments table.

Revision ID: 33e1b87b89d0
Revises: 1f08a0b4e0c3
Create Date: 2025-07-09 09:00:46.835603

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op
from app.enums.models.hospitalization_action_attachment_type_enums import (
    HospitalizationActionAttachmentType,
)

# revision identifiers, used by Alembic.
revision: str = "33e1b87b89d0"
down_revision: str | None = "1f08a0b4e0c3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "hospitalization_action_attachments",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("tenant_id", UUID(), nullable=False),
        sa.Column("hospitalization_action_id", UUID(), nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                HospitalizationActionAttachmentType,
                name="hospitalization_action_attachment_type_enum",
            ),
            nullable=False,
        ),
        sa.Column("file_name", sa.String(length=255), nullable=False),
        sa.Column("file_path", sa.String(length=255), nullable=False),
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
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("hospitalization_action_attachments")
