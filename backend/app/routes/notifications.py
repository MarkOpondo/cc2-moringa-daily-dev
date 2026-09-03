from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils import iso_utc

from app.extensions import db
from app.models import Notification

notifications_bp = Blueprint('notifications', __name__)


def _current_user_id():
    identity = get_jwt_identity()
    if not identity:
        return None
    if isinstance(identity, dict):
        return int(identity.get("id"))
    return int(identity)


def _serialize(n):
    is_read = bool(getattr(n, "IsRead", False))
    created_at = iso_utc(n.CreatedAt) if getattr(n, "CreatedAt", None) else None
    content_id = getattr(n, "ContentID", None)
    return {
        "id": n.NotificationID,
        "message": n.Message,
        # camelCase + snake_case so any frontend style works
        "isRead": is_read,
        "is_read": is_read,
        "contentId": content_id,
        "content_id": content_id,
        "createdAt": created_at,
        "created_at": created_at,
    }


# Registered under /api/users/me/notifications
@notifications_bp.route('', methods=['GET'], strict_slashes=False)
@notifications_bp.route('/notifications', methods=['GET'], strict_slashes=False)
@notifications_bp.route('/users/me/notifications', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_notifications():
    try:
        user_id = _current_user_id()
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid user identity"}), 400

    notifications = (
        Notification.query.filter_by(UserID=user_id)
        .order_by(Notification.NotificationID.desc())
        .all()
    )

    return jsonify([_serialize(n) for n in notifications]), 200


@notifications_bp.route('/unread-count', methods=['GET'], strict_slashes=False)
@jwt_required()
def unread_count():
    try:
        user_id = _current_user_id()
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid user identity"}), 400

    count = (
        Notification.query.filter_by(UserID=user_id, IsRead=False).count()
    )
    return jsonify({"count": count, "unreadCount": count}), 200


@notifications_bp.route('/<int:notification_id>/read', methods=['PATCH'], strict_slashes=False)
@jwt_required()
def mark_notification_read(notification_id):
    try:
        user_id = _current_user_id()
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid user identity"}), 400

    notification = db.session.get(Notification, notification_id)
    if not notification or notification.UserID != user_id:
        return jsonify({"error": "Notification not found"}), 404

    notification.IsRead = True
    db.session.commit()

    return jsonify({"message": "Notification marked as read.", **_serialize(notification)}), 200


@notifications_bp.route('/read-all', methods=['PATCH'], strict_slashes=False)
@jwt_required()
def mark_all_notifications_read():
    try:
        user_id = _current_user_id()
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid user identity"}), 400

    updated = (
        Notification.query
        .filter_by(UserID=user_id, IsRead=False)
        .update({"IsRead": True})
    )
    db.session.commit()

    return jsonify({"message": "All notifications marked as read.", "updated": updated}), 200
