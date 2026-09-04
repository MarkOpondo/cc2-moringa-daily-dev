"""Repair canonical columns omitted by older local databases.

Revision ID: a1b2c3d4e5f6
Revises: 9e8f4a1c2b3d
"""
from alembic import op
import sqlalchemy as sa


revision = "a1b2c3d4e5f6"
down_revision = "9e8f4a1c2b3d"
branch_labels = None
depends_on = None


CONTENT_COLUMNS = {
    "Summary": sa.Text(),
    "ThumbnailURL": sa.String(length=255),
    "Duration": sa.String(length=50),
    "ViewsCount": sa.Integer(),
    "LikesCount": sa.Integer(),
    "Hashtags": sa.String(length=255),
    "RejectionReason": sa.Text(),
}


def upgrade():
    existing = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("content")}
    missing = set(CONTENT_COLUMNS) - existing
    if not missing:
        return

    with op.batch_alter_table("content", schema=None) as batch_op:
        for name, column_type in CONTENT_COLUMNS.items():
            if name in missing:
                batch_op.add_column(sa.Column(name, column_type, nullable=True))


def downgrade():
    existing = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("content")}
    with op.batch_alter_table("content", schema=None) as batch_op:
        for name in reversed(tuple(CONTENT_COLUMNS)):
            if name in existing:
                batch_op.drop_column(name)
