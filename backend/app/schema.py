from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from models import (User, Profile, Category,Content, Comment, CommentReaction, ContentReaction,
                    Subscription,Wishlist,Share,Notification,ContentReport
                    )
from app import db

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        include_fk = True

class ProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Profile
        load_instance = True
        sqla_session = db.session
        include_fk = True


class CategorySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
        sqla_session = db.session
        include_fk = True


class ContentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Content
        load_instance = True
        sqla_session = db.session
        include_relationships = True
        include_fk = True


class CommentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Comment
        load_instance = True
        sqla_session = db.session
        include_fk = True


class ContentReactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ContentReaction
        load_instance = True
        sqla_session = db.session
        include_fk = True


class CommentReactionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CommentReaction
        load_instance = True
        sqla_session = db.session
        include_fk = True


class SubscriptionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Subscription
        load_instance = True
        sqla_session = db.session
        include_fk = True


class WishlistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Wishlist
        load_instance = True
        sqla_session = db.session
        include_fk = True


class ShareSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Share
        load_instance = True
        sqla_session = db.session
        include_fk = True


class NotificationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Notification
        load_instance = True
        sqla_session = db.session
        include_fk = True


class ContentReportSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ContentReport
        load_instance = True
        sqla_session = db.session
        include_fk = True