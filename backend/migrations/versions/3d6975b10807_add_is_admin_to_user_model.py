"""Add legacy moderation metadata columns.

Revision ID: 3d6975b10807
Revises: 7760eec6ebb1
Create Date: 2026-08-26 08:29:26.344103
"""
from alembic import op
import sqlalchemy as sa


revision = "3d6975b10807"
down_revision = "7760eec6ebb1"
branch_labels = None
depends_on = None


def upgrade():
    content_columns = {
        column["name"] for column in sa.inspect(op.get_bind()).get_columns("content")
    }
    user_columns = {
        column["name"] for column in sa.inspect(op.get_bind()).get_columns("users")
    }

    if "RejectionReason" not in content_columns:
        with op.batch_alter_table("content", schema=None) as batch_op:
            batch_op.add_column(sa.Column("RejectionReason", sa.Text(), nullable=True))

    if "is_admin" not in user_columns:
        with op.batch_alter_table("users", schema=None) as batch_op:
            batch_op.add_column(
                sa.Column("is_admin", sa.Boolean(), nullable=False, server_default="false")
            )


def downgrade():
    content_columns = {
        column["name"] for column in sa.inspect(op.get_bind()).get_columns("content")
    }
    user_columns = {
        column["name"] for column in sa.inspect(op.get_bind()).get_columns("users")
    }

    if "is_admin" in user_columns:
        with op.batch_alter_table("users", schema=None) as batch_op:
            batch_op.drop_column("is_admin")
    if "RejectionReason" in content_columns:
        with op.batch_alter_table("content", schema=None) as batch_op:
            batch_op.drop_column("RejectionReason")
