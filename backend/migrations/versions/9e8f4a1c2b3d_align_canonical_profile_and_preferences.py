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


def _unique_constraint_names(table_name):
    return {
        constraint.get("name")
        for constraint in sa.inspect(op.get_bind()).get_unique_constraints(table_name)
    }


def upgrade():
    # Normalize values written by the legacy route stacks before the
    # canonical API starts reading roles and reaction types.
    inspector = sa.inspect(op.get_bind())
    tables = set(inspector.get_table_names())
    if "users" in tables:
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
    if "content_reactions" in tables:
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
    if "comment_reactions" in tables:
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

    profile_columns = {
        column["name"] for column in inspector.get_columns("profiles")
    }
    missing_profile_columns = {"Skills", "GithubURL"} - profile_columns
    if missing_profile_columns:
        with op.batch_alter_table("profiles", schema=None) as batch_op:
            if "Skills" in missing_profile_columns:
                batch_op.add_column(sa.Column("Skills", sa.Text(), nullable=True))
            if "GithubURL" in missing_profile_columns:
                batch_op.add_column(sa.Column("GithubURL", sa.String(length=255), nullable=True))

    if "unique_user_username" not in _unique_constraint_names("users"):
        with op.batch_alter_table("users", schema=None) as batch_op:
            batch_op.create_unique_constraint("unique_user_username", ["Username"])

    if "unique_user_category_subscription" not in _unique_constraint_names("subscriptions"):
        with op.batch_alter_table("subscriptions", schema=None) as batch_op:
            batch_op.create_unique_constraint(
                "unique_user_category_subscription", ["UserID", "CategoryID"]
            )

    if "unique_user_content_wishlist" not in _unique_constraint_names("wishlist"):
        with op.batch_alter_table("wishlist", schema=None) as batch_op:
            batch_op.create_unique_constraint(
                "unique_user_content_wishlist", ["UserID", "ContentID"]
            )


def downgrade():
    for table_name, constraint_name in (
        ("wishlist", "unique_user_content_wishlist"),
        ("subscriptions", "unique_user_category_subscription"),
        ("users", "unique_user_username"),
    ):
        if constraint_name in _unique_constraint_names(table_name):
            with op.batch_alter_table(table_name, schema=None) as batch_op:
                batch_op.drop_constraint(constraint_name, type_="unique")

    profile_columns = {
        column["name"] for column in sa.inspect(op.get_bind()).get_columns("profiles")
    }
    with op.batch_alter_table("profiles", schema=None) as batch_op:
        if "GithubURL" in profile_columns:
            batch_op.drop_column("GithubURL")
        if "Skills" in profile_columns:
            batch_op.drop_column("Skills")
