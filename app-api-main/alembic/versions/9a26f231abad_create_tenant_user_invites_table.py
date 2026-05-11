"""create tenant user invites table.

Revision ID: 9a26f231abad
Revises: 33e1b87b89d0
Create Date: 2025-08-28 18:42:04.844096

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from alembic import op
from app.enums.models.tenant_user_invite_status_enum import TenantUserInviteStatusEnum

# revision identifiers, used by Alembic.
revision: str = "9a26f231abad"
down_revision: str | None = "33e1b87b89d0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tenant_user_invites",
        sa.Column(
            "id", UUID(), nullable=False, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("tenant_id", UUID(), nullable=False),
        sa.Column("role_id", UUID(), nullable=True),
        sa.Column("email", sa.String(length=150), nullable=True),
        sa.Column(
            "status",
            sa.Enum(TenantUserInviteStatusEnum, name="tenant_user_invite_status_enum"),
            default=TenantUserInviteStatusEnum.PENDING,
            nullable=False,
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
        sa.ForeignKeyConstraint(
            ["tenant_id"], ["tenants.id"], name="fk_tenant_user_invites_tenant"
        ),
        sa.ForeignKeyConstraint(
            ["role_id"], ["roles.id"], name="fk_tenant_user_invites_role"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tenant_user_invites")
