"""Add media metadata columns to the content table.

Revision ID: 7760eec6ebb1
Revises: 000000000001
Create Date: 2026-08-25 05:21:24.438385
"""
from alembic import op
import sqlalchemy as sa


revision = "7760eec6ebb1"
down_revision = "000000000001"
branch_labels = None
depends_on = None


def upgrade():
    columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("content")}
    missing = {"Duration", "ViewsCount", "Hashtags"} - columns
    if not missing:
        return

    with op.batch_alter_table("content", schema=None) as batch_op:
        if "Duration" in missing:
            batch_op.add_column(sa.Column("Duration", sa.String(length=50), nullable=True))
        if "ViewsCount" in missing:
            batch_op.add_column(sa.Column("ViewsCount", sa.Integer(), nullable=True))
        if "Hashtags" in missing:
            batch_op.add_column(sa.Column("Hashtags", sa.String(length=255), nullable=True))


def downgrade():
    columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("content")}
    with op.batch_alter_table("content", schema=None) as batch_op:
        if "Hashtags" in columns:
            batch_op.drop_column("Hashtags")
        if "ViewsCount" in columns:
            batch_op.drop_column("ViewsCount")
        if "Duration" in columns:
            batch_op.drop_column("Duration")
