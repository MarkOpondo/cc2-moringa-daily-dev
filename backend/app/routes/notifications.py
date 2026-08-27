from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Notification

notifications_bp = Blueprint("notifications", __name__)

@notifications_bp.get("")
@jwt_required()
def get_notifications():
    notifs = Notification.query.filter_by(
        UserID=int(get_jwt_identity())
    ).order_by(Notification.CreatedAt.desc()).all()

    return jsonify([{
        "id": notification.NotificationID,
        "message": notification.Message,
        "is_read": notification.IsRead,
        "created_at": (
            notification.CreatedAt.isoformat()
             if notification.CreatedAt 
             else None
             ),
    }for notification in notifs]),200
#--------------------- MARK AS READ -------------------
@notifications_bp.patch("/<int:notification_id>/read")
@jwt_required()
def mark_as_read(notification_id):
    notif = Notification.query.get_or_404(notification_id)

    if notif.UserID != int(get_jwt_identity()):
        return jsonify({"error": "Forbidden"}),403
    notif.IsRead=True
    db.session.commit()
    return jsonify({
        "message": "Notification marked as read. "}), 200    