"""Align profile and preference constraints with the canonical API.

Revision ID: 9e8f4a1c2b3d
Revises: 005a7387fadb
"""
from alembic import op
import sqlalchemy as sa


revision = "9e8f4a1c2b3d"
down_revision = "005a7387fadb"
branch_labels = None
depends_on = None


def upgrade():
    # Normalize values written by the legacy route stacks before the
    # canonical API starts reading roles and reaction types.
    op.execute(
        sa.text(
            """
            UPDATE "users"
            SET "Role" = CASE
                WHEN lower(trim(coalesce("Role", ''))) IN ('admin', 'administrator') THEN 'admin'
                WHEN lower(trim(coalesce("Role", ''))) IN ('tech writer', 'tech_writer', 'tech-writer', 'techwriter') THEN 'tech_writer'
                ELSE 'user'
            END,
            "IsActive" = coalesce("IsActive", TRUE)
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE "content_reactions"
            SET "Reaction" = CASE
                WHEN lower(trim("Reaction")) = 'like' THEN 'like'
                ELSE 'dislike'
            END
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE "comment_reactions"
            SET "Reaction" = CASE
                WHEN lower(trim("Reaction")) = 'like' THEN 'like'
                ELSE 'dislike'
            END
            """
        )
    )

    with op.batch_alter_table("profiles", schema=None) as batch_op:
        batch_op.add_column(sa.Column("Skills", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("GithubURL", sa.String(length=255), nullable=True))

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_unique_constraint("unique_user_username", ["Username"])

    with op.batch_alter_table("subscriptions", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            "unique_user_category_subscription", ["UserID", "CategoryID"]
        )

    with op.batch_alter_table("wishlist", schema=None) as batch_op:
        batch_op.create_unique_constraint(
            "unique_user_content_wishlist", ["UserID", "ContentID"]
        )


def downgrade():
    with op.batch_alter_table("wishlist", schema=None) as batch_op:
        batch_op.drop_constraint("unique_user_content_wishlist", type_="unique")

    with op.batch_alter_table("subscriptions", schema=None) as batch_op:
        batch_op.drop_constraint("unique_user_category_subscription", type_="unique")

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint("unique_user_username", type_="unique")

    with op.batch_alter_table("profiles", schema=None) as batch_op:
        batch_op.drop_column("GithubURL")
        batch_op.drop_column("Skills")
