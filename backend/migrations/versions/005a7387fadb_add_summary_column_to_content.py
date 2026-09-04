"""Add summary and thumbnail columns to content.

Revision ID: 005a7387fadb
Revises: d8ccba26a441
Create Date: 2026-08-26 17:10:42.102085
"""
from alembic import op
import sqlalchemy as sa


revision = "005a7387fadb"
down_revision = "d8ccba26a441"
branch_labels = None
depends_on = None


def upgrade():
    columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("content")}
    missing = {"Summary", "ThumbnailURL"} - columns
    if not missing:
        return

    with op.batch_alter_table("content", schema=None) as batch_op:
        if "Summary" in missing:
            batch_op.add_column(sa.Column("Summary", sa.Text(), nullable=True))
        if "ThumbnailURL" in missing:
            batch_op.add_column(sa.Column("ThumbnailURL", sa.String(length=255), nullable=True))


def downgrade():
    columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("content")}
    with op.batch_alter_table("content", schema=None) as batch_op:
        if "ThumbnailURL" in columns:
            batch_op.drop_column("ThumbnailURL")
        if "Summary" in columns:
            batch_op.drop_column("Summary")
