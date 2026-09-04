"""Create the initial Moringa Daily Dev schema.

Revision ID: 000000000001
Revises: None
"""
from alembic import op
import sqlalchemy as sa


revision = "000000000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("UserID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("Username", sa.String(length=150), nullable=False),
        sa.Column("Email", sa.String(length=200), nullable=False),
        sa.Column("_Password_Hash", sa.String(), nullable=False),
        sa.Column("Role", sa.String(length=50), nullable=False, server_default="user"),
        sa.Column("IsActive", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("UserID"),
        sa.UniqueConstraint("Email"),
    )
    op.create_table(
        "profiles",
        sa.Column("ProfileID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("UserID", sa.Integer(), nullable=False),
        sa.Column("Bio", sa.Text(), nullable=True),
        sa.Column("ProfileImage", sa.String(length=255), nullable=True),
        sa.Column("Interests", sa.Text(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
        sa.Column("UpdatedAt", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["UserID"], ["users.UserID"]),
        sa.PrimaryKeyConstraint("ProfileID"),
        sa.UniqueConstraint("UserID"),
    )
    op.create_table(
        "categories",
        sa.Column("CategoryID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("Name", sa.String(length=100), nullable=False),
        sa.Column("Description", sa.Text(), nullable=True),
        sa.Column("CreatedBy", sa.Integer(), nullable=True),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["CreatedBy"], ["users.UserID"]),
        sa.PrimaryKeyConstraint("CategoryID"),
        sa.UniqueConstraint("Name"),
    )
    op.create_table(
        "content",
        sa.Column("ContentID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("UserID", sa.Integer(), nullable=False),
        sa.Column("Title", sa.String(length=255), nullable=False),
        sa.Column("Description", sa.Text(), nullable=True),
        sa.Column("ContentType", sa.String(length=50), nullable=False, server_default="Article"),
        sa.Column("ContentURL", sa.String(length=255), nullable=True),
        sa.Column("Status", sa.String(length=50), nullable=False, server_default="Draft"),
        sa.Column("IsApproved", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
        sa.Column("UpdatedAt", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            '"Status" IN (\'Draft\', \'Published\', \'Archived\')',
            name="check_valid_content_status",
        ),
        sa.CheckConstraint(
            '"ContentType" IN (\'Article\', \'Video\', \'Audio\', \'Image\')',
            name="check_valid_content_type",
        ),
        sa.ForeignKeyConstraint(["UserID"], ["users.UserID"]),
        sa.PrimaryKeyConstraint("ContentID"),
    )
    op.create_table(
        "content_categories",
        sa.Column("ContentID", sa.Integer(), nullable=False),
        sa.Column("CategoryID", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["CategoryID"], ["categories.CategoryID"]),
        sa.ForeignKeyConstraint(["ContentID"], ["content.ContentID"]),
        sa.PrimaryKeyConstraint("ContentID", "CategoryID"),
    )
    op.create_table(
        "comments",
        sa.Column("CommentID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("UserID", sa.Integer(), nullable=False),
        sa.Column("ContentID", sa.Integer(), nullable=False),
        sa.Column("ParentCommentID", sa.Integer(), nullable=True),
        sa.Column("Text", sa.Text(), nullable=False),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
        sa.Column("UpdatedAt", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            '"CommentID" != "ParentCommentID"',
            name="check_no_self_parenting_comment",
        ),
        sa.CheckConstraint('length(trim("Text")) > 0', name="check_comment_not_empty"),
        sa.ForeignKeyConstraint(["ContentID"], ["content.ContentID"]),
        sa.ForeignKeyConstraint(["ParentCommentID"], ["comments.CommentID"]),
        sa.ForeignKeyConstraint(["UserID"], ["users.UserID"]),
        sa.PrimaryKeyConstraint("CommentID"),
    )
    op.create_table(
        "content_reactions",
        sa.Column("ReactionID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("UserID", sa.Integer(), nullable=False),
        sa.Column("ContentID", sa.Integer(), nullable=False),
        sa.Column("Reaction", sa.String(length=50), nullable=False),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["ContentID"], ["content.ContentID"]),
        sa.ForeignKeyConstraint(["UserID"], ["users.UserID"]),
        sa.PrimaryKeyConstraint("ReactionID"),
        sa.UniqueConstraint("UserID", "ContentID", name="unique_user_content_reaction"),
    )
    op.create_index(
        "ix_content_reaction_lookup", "content_reactions", ["ContentID", "Reaction"]
    )
    op.create_table(
        "comment_reactions",
        sa.Column("ReactionID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("UserID", sa.Integer(), nullable=False),
        sa.Column("CommentID", sa.Integer(), nullable=False),
        sa.Column("Reaction", sa.String(length=50), nullable=False),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["CommentID"], ["comments.CommentID"]),
        sa.ForeignKeyConstraint(["UserID"], ["users.UserID"]),
        sa.PrimaryKeyConstraint("ReactionID"),
        sa.UniqueConstraint("UserID", "CommentID", name="unique_user_comment_reaction"),
    )
    op.create_index(
        "ix_comment_reaction_lookup", "comment_reactions", ["CommentID", "Reaction"]
    )
    op.create_table(
        "subscriptions",
        sa.Column("SubscriptionID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("UserID", sa.Integer(), nullable=False),
        sa.Column("CategoryID", sa.Integer(), nullable=False),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["CategoryID"], ["categories.CategoryID"]),
        sa.ForeignKeyConstraint(["UserID"], ["users.UserID"]),
        sa.PrimaryKeyConstraint("SubscriptionID"),
    )
    op.create_table(
        "wishlist",
        sa.Column("WishlistID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("UserID", sa.Integer(), nullable=False),
        sa.Column("ContentID", sa.Integer(), nullable=False),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["ContentID"], ["content.ContentID"]),
        sa.ForeignKeyConstraint(["UserID"], ["users.UserID"]),
        sa.PrimaryKeyConstraint("WishlistID"),
    )
    op.create_table(
        "shares",
        sa.Column("ShareID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("UserID", sa.Integer(), nullable=False),
        sa.Column("ContentID", sa.Integer(), nullable=False),
        sa.Column("SharedWithUserID", sa.Integer(), nullable=False),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["ContentID"], ["content.ContentID"]),
        sa.ForeignKeyConstraint(["SharedWithUserID"], ["users.UserID"]),
        sa.ForeignKeyConstraint(["UserID"], ["users.UserID"]),
        sa.PrimaryKeyConstraint("ShareID"),
    )
    op.create_table(
        "notifications",
        sa.Column("NotificationID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("UserID", sa.Integer(), nullable=False),
        sa.Column("ContentID", sa.Integer(), nullable=True),
        sa.Column("Message", sa.Text(), nullable=False),
        sa.Column("IsRead", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["ContentID"], ["content.ContentID"]),
        sa.ForeignKeyConstraint(["UserID"], ["users.UserID"]),
        sa.PrimaryKeyConstraint("NotificationID"),
    )
    op.create_table(
        "content_reports",
        sa.Column("ReportID", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("ContentID", sa.Integer(), nullable=False),
        sa.Column("ReportedBy", sa.Integer(), nullable=False),
        sa.Column("Reason", sa.Text(), nullable=False),
        sa.Column("Status", sa.String(length=50), nullable=False, server_default="Pending"),
        sa.Column("CreatedAt", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["ContentID"], ["content.ContentID"]),
        sa.ForeignKeyConstraint(["ReportedBy"], ["users.UserID"]),
        sa.PrimaryKeyConstraint("ReportID"),
    )


def downgrade():
    op.drop_table("content_reports")
    op.drop_table("notifications")
    op.drop_table("shares")
    op.drop_table("wishlist")
    op.drop_table("subscriptions")
    op.drop_index("ix_comment_reaction_lookup", table_name="comment_reactions")
    op.drop_table("comment_reactions")
    op.drop_index("ix_content_reaction_lookup", table_name="content_reactions")
    op.drop_table("content_reactions")
    op.drop_table("comments")
    op.drop_table("content_categories")
    op.drop_table("content")
    op.drop_table("categories")
    op.drop_table("profiles")
    op.drop_table("users")
