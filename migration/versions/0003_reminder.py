"""Add reminder settings to users table

Revision ID: 0003_reminder
Revises: 0002_add_platform_to_users
Create Date: 2024-03-30
"""
from alembic import op
import sqlalchemy as sa

revision = "0003_reminder"
down_revision = "0002_add_platform_to_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("reminder_hour", sa.Integer(), nullable=True))
    op.add_column("users", sa.Column("reminder_enabled", sa.Boolean(), nullable=False, server_default="false"))
    op.create_index(op.f("ix_users_reminder_hour"), "users", ["reminder_hour"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_users_reminder_hour"), table_name="users")
    op.drop_column("users", "reminder_enabled")
    op.drop_column("users", "reminder_hour")