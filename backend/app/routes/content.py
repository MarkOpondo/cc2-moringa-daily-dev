from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from sqlalchemy import or_

from app.extensions import db
from app.models import Category, Content, Notification, Subscription, User, normalized_role
from app.serializers import serialize_content


content_bp = Blueprint("content", __name__)

CONTENT_TYPES = {"article": "Article", "video": "Video", "audio": "Audio", "image": "Image"}
CONTENT_STATUSES = {"draft": "Draft", "published": "Published", "archived": "Archived"}


def _current_user():
    identity = get_jwt_identity()
    return db.session.get(User, int(identity)) if identity is not None else None


def _is_moderator(user):
    return user and normalized_role(user.Role) in {"admin", "tech_writer"}


def _type_value(value):
    return CONTENT_TYPES.get(str(value or "").strip().lower())


def _status_value(value):
    return CONTENT_STATUSES.get(str(value or "").strip().lower())


def _notify_subscribers(content_item):
    recipient_ids = set()
    for category in content_item.categories:
        subscriptions = Subscription.query.filter_by(CategoryID=category.CategoryID).all()
        recipient_ids.update(subscription.UserID for subscription in subscriptions)

    recipient_ids.discard(content_item.UserID)
    for user_id in recipient_ids:
        db.session.add(
            Notification(
                UserID=user_id,
                ContentID=content_item.ContentID,
                Message=f"New content in your feed: '{content_item.Title}'",
            )
        )


def _viewer_for_content(item):
    """Resolve an optional viewer and enforce public/private visibility."""
    verify_jwt_in_request(optional=True)
    user = _current_user()
    is_public = item.Status == "Published" and item.IsApproved
    can_view_private = user and (user.UserID == item.UserID or _is_moderator(user))
    return user, is_public or bool(can_view_private)


@content_bp.get("")
def list_content():
    category_id = request.args.get("category", type=int)
    search = request.args.get("search", "").strip()
    requested_status = request.args.get("status")

    query = Content.query.filter(Content.Status == "Published", Content.IsApproved.is_(True))
    if requested_status and _status_value(requested_status) != "Published":
        return jsonify({"error": "Only published content is available in the public feed"}), 400
    if category_id:
        query = query.filter(Content.categories.any(Category.CategoryID == category_id))
    if search:
        pattern = f"%{search}%"
        query = query.filter(or_(Content.Title.ilike(pattern), Content.Description.ilike(pattern)))

    items = query.order_by(Content.CreatedAt.desc()).all()
    return jsonify([serialize_content(item, include_private=False) for item in items]), 200


@content_bp.get("/<int:content_id>")
def get_single_content(content_id):
    item = db.session.get(Content, content_id)
    if not item:
        return jsonify({"error": "Content not found"}), 404

    user, can_view = _viewer_for_content(item)
    if not can_view:
        return jsonify({"error": "Content not found"}), 404

    is_private_view = user and (user.UserID == item.UserID or _is_moderator(user))
    return jsonify(serialize_content(item, include_private=bool(is_private_view))), 200


@content_bp.post("")
@jwt_required()
def create_content():
    user = _current_user()
    if not user or not user.IsActive:
        return jsonify({"error": "Active user account required"}), 403

    data = request.get_json(silent=True) or {}
    title = str(data.get("title") or "").strip()
    body = str(data.get("body", data.get("description")) or "").strip()
    content_type = _type_value(data.get("type", data.get("content_type")))
    category_id = data.get("categoryId", data.get("category_id"))

    if not title or not body or not content_type or not category_id:
        return jsonify({"error": "title, body, type, and categoryId are required"}), 400
    if len(title) > 255:
        return jsonify({"error": "Title is too long"}), 400

    try:
        category_id = int(category_id)
    except (TypeError, ValueError):
        return jsonify({"error": "categoryId must be an integer"}), 400

    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    item = Content(
        UserID=user.UserID,
        Title=title,
        Description=body,
        ContentType=content_type,
        ContentURL=data.get("mediaUrl", data.get("url")) or None,
        Summary=data.get("summary"),
        ThumbnailURL=data.get("thumbnailUrl", data.get("thumbnail_url")),
        Duration=str(data["duration"]) if data.get("duration") is not None else None,
        Hashtags=data.get("hashtags"),
        Status="Draft",
        IsApproved=False,
    )
    item.categories.append(category)
    db.session.add(item)
    db.session.commit()
    return jsonify(serialize_content(item)), 201


@content_bp.patch("/<int:content_id>")
@jwt_required()
def edit_content(content_id):
    item = db.session.get(Content, content_id)
    user = _current_user()
    if not item:
        return jsonify({"error": "Content not found"}), 404
    if not user or (item.UserID != user.UserID and not _is_moderator(user)):
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json(silent=True) or {}
    if "title" in data:
        title = str(data["title"] or "").strip()
        if not title or len(title) > 255:
            return jsonify({"error": "Title must be between 1 and 255 characters"}), 400
        item.Title = title
    if "body" in data or "description" in data:
        item.Description = str(data.get("body", data.get("description")) or "").strip()
        if not item.Description:
            return jsonify({"error": "Content body cannot be empty"}), 400
    if "type" in data or "content_type" in data:
        content_type = _type_value(data.get("type", data.get("content_type")))
        if not content_type:
            return jsonify({"error": "Unsupported content type"}), 400
        item.ContentType = content_type
    if "mediaUrl" in data or "url" in data:
        item.ContentURL = data.get("mediaUrl", data.get("url")) or None
    if "categoryId" in data or "category_id" in data:
        category = db.session.get(Category, data.get("categoryId", data.get("category_id")))
        if not category:
            return jsonify({"error": "Category not found"}), 404
        item.categories = [category]

    db.session.commit()
    return jsonify(serialize_content(item)), 200


@content_bp.delete("/<int:content_id>")
@jwt_required()
def delete_content(content_id):
    item = db.session.get(Content, content_id)
    user = _current_user()
    if not item:
        return jsonify({"error": "Content not found"}), 404
    if not user or (item.UserID != user.UserID and normalized_role(user.Role) != "admin"):
        return jsonify({"error": "Forbidden"}), 403
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Content deleted"}), 200
