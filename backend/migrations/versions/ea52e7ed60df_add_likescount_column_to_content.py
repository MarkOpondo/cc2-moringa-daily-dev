"""Add LikesCount column to Content.

Revision ID: ea52e7ed60df
Revises: 3d6975b10807
Create Date: 2026-08-26 11:21:20.006082
"""
from alembic import op
import sqlalchemy as sa


revision = "ea52e7ed60df"
down_revision = "3d6975b10807"
branch_labels = None
depends_on = None


def upgrade():
    columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("content")}
    if "LikesCount" not in columns:
        with op.batch_alter_table("content", schema=None) as batch_op:
            batch_op.add_column(
                sa.Column("LikesCount", sa.Integer(), nullable=False, server_default="0")
            )


def downgrade():
    columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("content")}
    if "LikesCount" in columns:
        with op.batch_alter_table("content", schema=None) as batch_op:
            batch_op.drop_column("LikesCount")
