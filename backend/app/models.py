from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Index, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property

from app.extensions import bcrypt, db


ROLE_ALIASES = {
    "administrator": "admin",
    "tech writer": "tech_writer",
    "tech-writer": "tech_writer",
    "techwriter": "tech_writer",
    "member": "user",
}


def normalized_role(value):
    role = str(value or "user").strip().lower().replace("_", " ")
    return ROLE_ALIASES.get(role, role.replace(" ", "_"))


content_categories = db.Table(
    "content_categories",
    db.Column("ContentID", db.Integer, db.ForeignKey("content.ContentID"), primary_key=True),
    db.Column("CategoryID", db.Integer, db.ForeignKey("categories.CategoryID"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(150), unique=True, nullable=False)
    Email = db.Column(db.String(200), unique=True, nullable=False)
    _Password_Hash = db.Column(db.String, nullable=False)
    Role = db.Column(db.String(50), nullable=False, default="user")
    IsActive = db.Column(db.Boolean, nullable=False, default=True)
    CreatedAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    profile = db.relationship(
        "Profile", backref="user", uselist=False, cascade="all, delete-orphan"
    )
    categories_created = db.relationship(
        "Category", backref="creator", foreign_keys="Category.CreatedBy"
    )
    contents = db.relationship("Content", backref="author", foreign_keys="Content.UserID")
    comments = db.relationship("Comment", backref="author", foreign_keys="Comment.UserID")
    content_reactions = db.relationship("ContentReaction", backref="user")
    comment_reactions = db.relationship("CommentReaction", backref="user")
    subscriptions = db.relationship("Subscription", backref="user")
    wishlist_items = db.relationship("Wishlist", backref="user")
    shares_sent = db.relationship("Share", foreign_keys="Share.UserID", backref="sender")
    shares_received = db.relationship(
        "Share", foreign_keys="Share.SharedWithUserID", backref="recipient"
    )
    notifications = db.relationship("Notification", backref="user")
    reports_submitted = db.relationship("ContentReport", backref="reporter")

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._Password_Hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._Password_Hash, password.encode("utf-8"))


class Profile(db.Model):
    __tablename__ = "profiles"

    ProfileID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey("users.UserID"), unique=True, nullable=False)
    Bio = db.Column(db.Text, nullable=True)
    ProfileImage = db.Column(db.String(255), nullable=True)
    Interests = db.Column(db.Text, nullable=True)
    Skills = db.Column(db.Text, nullable=True)
    GithubURL = db.Column(db.String(255), nullable=True)
    CreatedAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    UpdatedAt = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class Category(db.Model):
    __tablename__ = "categories"

    CategoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(100), unique=True, nullable=False)
    Description = db.Column(db.Text, nullable=True)
    CreatedBy = db.Column(db.Integer, db.ForeignKey("users.UserID"), nullable=True)
    CreatedAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    subscribers = db.relationship("Subscription", backref="category")


class Content(db.Model):
    __tablename__ = "content"

    ContentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey("users.UserID"), nullable=False)
    Title = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    ContentType = db.Column(db.String(50), nullable=False, default="Article")
    ContentURL = db.Column(db.String(255), nullable=True)
    Summary = db.Column(db.Text, nullable=True)
    ThumbnailURL = db.Column(db.String(255), nullable=True)
    Duration = db.Column(db.String(50), nullable=True)
    ViewsCount = db.Column(db.Integer, nullable=False, default=0)
    LikesCount = db.Column(db.Integer, nullable=False, default=0)
    Hashtags = db.Column(db.String(255), nullable=True)
    RejectionReason = db.Column(db.Text, nullable=True)
    Status = db.Column(db.String(50), nullable=False, default="Draft")
    IsApproved = db.Column(db.Boolean, nullable=False, default=False)
    CreatedAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    UpdatedAt = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    categories = db.relationship(
        "Category",
        secondary=content_categories,
        backref=db.backref("contents", lazy="dynamic"),
    )
    comments = db.relationship("Comment", backref="content", cascade="all, delete-orphan")
    reactions = db.relationship(
        "ContentReaction", backref="content", cascade="all, delete-orphan"
    )
    wishlists = db.relationship("Wishlist", backref="content", cascade="all, delete-orphan")
    shares = db.relationship("Share", backref="content", cascade="all, delete-orphan")
    notifications = db.relationship(
        "Notification", backref="content", cascade="all, delete-orphan"
    )
    reports = db.relationship(
        "ContentReport", backref="content", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            '"Status" IN (\'Draft\', \'Published\', \'Archived\')',
            name="check_valid_content_status",
        ),
        CheckConstraint(
            '"ContentType" IN (\'Article\', \'Video\', \'Audio\', \'Image\')',
            name="check_valid_content_type",
        ),
    )


class Comment(db.Model):
    __tablename__ = "comments"

    CommentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey("users.UserID"), nullable=False)
    ContentID = db.Column(db.Integer, db.ForeignKey("content.ContentID"), nullable=False)
    ParentCommentID = db.Column(db.Integer, db.ForeignKey("comments.CommentID"), nullable=True)
    Text = db.Column(db.Text, nullable=False)
    CreatedAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    UpdatedAt = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    replies = db.relationship(
        "Comment",
        backref=db.backref("parent", remote_side=[CommentID]),
        cascade="all, delete-orphan",
    )
    reactions = db.relationship(
        "CommentReaction", backref="comment", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            '"CommentID" != "ParentCommentID"',
            name="check_no_self_parenting_comment",
        ),
        CheckConstraint(
            'length(trim("Text")) > 0',
            name="check_comment_not_empty",
        ),
    )


class ContentReaction(db.Model):
    __tablename__ = "content_reactions"

    ReactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey("users.UserID"), nullable=False)
    ContentID = db.Column(db.Integer, db.ForeignKey("content.ContentID"), nullable=False)
    Reaction = db.Column(db.String(50), nullable=False)
    CreatedAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("UserID", "ContentID", name="unique_user_content_reaction"),
        Index("ix_content_reaction_lookup", "ContentID", "Reaction"),
    )


class CommentReaction(db.Model):
    __tablename__ = "comment_reactions"

    ReactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey("users.UserID"), nullable=False)
    CommentID = db.Column(db.Integer, db.ForeignKey("comments.CommentID"), nullable=False)
    Reaction = db.Column(db.String(50), nullable=False)
    CreatedAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("UserID", "CommentID", name="unique_user_comment_reaction"),
        Index("ix_comment_reaction_lookup", "CommentID", "Reaction"),
    )


class Subscription(db.Model):
    __tablename__ = "subscriptions"

    SubscriptionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey("users.UserID"), nullable=False)
    CategoryID = db.Column(db.Integer, db.ForeignKey("categories.CategoryID"), nullable=False)
    CreatedAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("UserID", "CategoryID", name="unique_user_category_subscription"),
    )


class Wishlist(db.Model):
    __tablename__ = "wishlist"

    WishlistID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey("users.UserID"), nullable=False)
    ContentID = db.Column(db.Integer, db.ForeignKey("content.ContentID"), nullable=False)
    CreatedAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("UserID", "ContentID", name="unique_user_content_wishlist"),
    )


class Share(db.Model):
    __tablename__ = "shares"

    ShareID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey("users.UserID"), nullable=False)
    ContentID = db.Column(db.Integer, db.ForeignKey("content.ContentID"), nullable=False)
    SharedWithUserID = db.Column(db.Integer, db.ForeignKey("users.UserID"), nullable=False)
    CreatedAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Notification(db.Model):
    __tablename__ = "notifications"

    NotificationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey("users.UserID"), nullable=False)
    ContentID = db.Column(db.Integer, db.ForeignKey("content.ContentID"), nullable=True)
    Message = db.Column(db.Text, nullable=False)
    IsRead = db.Column(db.Boolean, nullable=False, default=False)
    CreatedAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class ContentReport(db.Model):
    __tablename__ = "content_reports"

    ReportID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ContentID = db.Column(db.Integer, db.ForeignKey("content.ContentID"), nullable=False)
    ReportedBy = db.Column(db.Integer, db.ForeignKey("users.UserID"), nullable=False)
    Reason = db.Column(db.Text, nullable=False)
    Status = db.Column(db.String(50), nullable=False, default="Pending")
    CreatedAt = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
