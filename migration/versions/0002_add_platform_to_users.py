"""Add platform column to users for multi-messenger support

Revision ID: 0002_add_platform_to_users
Revises: 0001_init
Create Date: 2025-01-15 12:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = "0002_add_platform_to_users"
down_revision = "0001_init"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.add_column(
        "users",
        sa.Column("platform", sa.String(32), nullable=False, server_default="telegram"),
    )

    op.add_column(
        "users",
        sa.Column("full_name", sa.String, nullable=True),
    )

    op.alter_column(
        "users",
        "external_id",
        existing_type=sa.Integer(),
        type_=sa.String(64),
        existing_nullable=False,
        postgresql_using="external_id::varchar",
    )

    op.alter_column(
        "users",
        "name",
        existing_type=sa.String(32),
        type_=sa.String(32),
        existing_nullable=False,
        new_column_name="username",
    )

    op.create_unique_constraint(
        "uq_platform_external_id", "users", ["platform", "external_id"]
    )
    op.create_index(
        "ix_platform_external_id", "users", ["platform", "external_id"], unique=False
    )

    op.execute("UPDATE users SET platform = 'telegram' WHERE platform = 'telegram'")


def downgrade() -> None:

    op.drop_index("ix_platform_created", table_name="users")
    op.drop_index("ix_platform_external_id", table_name="users")

    op.drop_constraint("uq_platform_external_id", "users", type_="unique")

    op.drop_column("users", "platform")

    op.alter_column(
        "users",
        "external_id",
        existing_type=sa.String(64),
        type_=sa.Integer(),
        existing_nullable=False,
        postgresql_using="external_id::integer",
    )
