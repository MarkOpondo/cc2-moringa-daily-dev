"""Add the legacy likes table if it is not already present.

Revision ID: d8ccba26a441
Revises: ea52e7ed60df
Create Date: 2026-08-26 15:07:33.294555
"""
from alembic import op
import sqlalchemy as sa


revision = "d8ccba26a441"
down_revision = "ea52e7ed60df"
branch_labels = None
depends_on = None


def upgrade():
    if "likes" in sa.inspect(op.get_bind()).get_table_names():
        return

    op.create_table(
        "likes",
        sa.Column("LikeID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("UserID", sa.Integer(), nullable=False),
        sa.Column("ContentID", sa.Integer(), nullable=False),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["ContentID"], ["content.ContentID"]),
        sa.ForeignKeyConstraint(["UserID"], ["users.UserID"]),
        sa.PrimaryKeyConstraint("LikeID"),
        sa.UniqueConstraint("UserID", "ContentID", name="unique_user_content_like"),
    )


def downgrade():
    if "likes" in sa.inspect(op.get_bind()).get_table_names():
        op.drop_table("likes")
