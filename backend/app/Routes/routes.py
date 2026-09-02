from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.extensions import db
from app.models import Category, Notification, User, Content as Post

bp = Blueprint("api", __name__)


# --------------------- Category Creation Route ---------------- #


@bp.post("/categories")
@jwt_required()
def create_category():
    data = request.get_json() or {}
    if "Name" not in data:
        return jsonify({"error": "Name is required"}), 400

    existing_category = Category.query.filter_by(Name=data["Name"]).first()
    if existing_category:
        return jsonify({"error": "Category with this name already exists"}), 400

    category = Category(Name=data["Name"], Description=data.get("Description"))
    db.session.add(category)
    db.session.commit()

    return (
        jsonify({
            "CategoryID": category.CategoryID,
            "Name": category.Name,
            "Description": category.Description,
        }),
        201,
    )


# --------------------- User Directory Route ------------------- #


@bp.get("/users")
def get_users():
    users = User.query.all()
    return (
        jsonify([
            {
                "UserID": u.UserID,
                "Username": u.Username,
                "Email": u.Email,
                "Role": getattr(u, "Role", "User"),
                "IsActive": getattr(u, "IsActive", True),
            }
            for u in users
        ]),
        200,
    )


# --------------------- Single Post Detail Route --------------- #


@bp.get("/posts/<int:post_id>")
def get_single_post(post_id):
    post = Post.query.get(post_id)
    
    if not post:
        return jsonify({"error": "Content not found"}), 404
        
    return jsonify({
        "id": getattr(post, "id", getattr(post, "ContentID", post_id)),
        "title": getattr(post, "title", getattr(post, "Title", "")),
        "description": getattr(post, "description", getattr(post, "Description", "")),
        "summary": getattr(post, "summary", getattr(post, "Summary", "")),
        "content_type": getattr(post, "content_type", getattr(post, "ContentType", "article")),
        "thumbnail_url": getattr(post, "thumbnail_url", getattr(post, "ThumbnailURL", "")),
        "created_at": getattr(post, "created_at", getattr(post, "CreatedAt", "")),
        "likes_count": getattr(post, "likes_count", getattr(post, "LikesCount", 0)),
        "views_count": getattr(post, "views_count", getattr(post, "ViewsCount", 0)),
        "hashtags": getattr(post, "hashtags", getattr(post, "Hashtags", "")),
        "duration": getattr(post, "duration", getattr(post, "Duration", 5)),
    }), 200


# --------------------- Notification Mark Read ----------------- #


@bp.patch("/notifications/<int:notification_id>/read")
@jwt_required()
def mark_notification_read(notification_id):
    try:
        current_user_id = int(get_jwt_identity())
    except (ValueError, TypeError):
        current_user_id = get_jwt_identity()

    notification = Notification.query.filter_by(
        NotificationID=notification_id, UserID=current_user_id
    ).first()

    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    notification.IsRead = True
    db.session.commit()
    return jsonify({"message": "Notification marked as read"}), 200