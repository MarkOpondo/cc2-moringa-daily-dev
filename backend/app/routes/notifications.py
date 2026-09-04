from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Notification


notifications_bp = Blueprint("notifications", __name__)


def _payload(notification):
    return {
        "id": notification.NotificationID,
        "message": notification.Message,
        "isRead": bool(notification.IsRead),
        "contentId": notification.ContentID,
        "createdAt": notification.CreatedAt.isoformat() if notification.CreatedAt else None,
    }


@notifications_bp.get("")
@jwt_required()
def get_notifications():
    user_id = int(get_jwt_identity())
    notifications = Notification.query.filter_by(UserID=user_id).order_by(
        Notification.CreatedAt.desc()
    ).all()
    return jsonify([_payload(notification) for notification in notifications]), 200


@notifications_bp.patch("/<int:notification_id>/read")
@jwt_required()
def mark_as_read(notification_id):
    notification = Notification.query.filter_by(
        NotificationID=notification_id, UserID=int(get_jwt_identity())
    ).first()
    if not notification:
        return jsonify({"error": "Notification not found"}), 404
    notification.IsRead = True
    db.session.commit()
    return jsonify(_payload(notification)), 200


@notifications_bp.patch("/read-all")
@jwt_required()
def mark_all_as_read():
    Notification.query.filter_by(UserID=int(get_jwt_identity()), IsRead=False).update(
        {Notification.IsRead: True}, synchronize_session=False
    )
    db.session.commit()
    return jsonify({"message": "All notifications marked as read"}), 200
