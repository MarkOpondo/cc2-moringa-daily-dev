from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.models import Content, Notification, User
from . import content_bp


@content_bp.get("/admin/pending")
@jwt_required()
def get_pending_content():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Bulletproof admin check (checks both is_admin attribute and Role string)
    is_admin = getattr(user, "is_admin", False)
    if not is_admin and hasattr(user, "Role") and user.Role:
        is_admin = user.Role.lower() == "admin"

    if not user or not is_admin:
        return jsonify({"error": "Access forbidden: Admin privileges required"}), 403

    pending_items = (
        Content.query.filter_by(Status="Pending")
        .order_by(Content.CreatedAt.desc())
        .all()
    )

    pending_data = []
    for item in pending_items:
        pending_data.append(
            {
                "content_id": item.ContentID,
                "title": item.Title,
                "description": item.Description,
                "content_type": item.ContentType,
                "content_url": item.ContentURL,
                "duration": item.Duration,
                "created_at": (
                    item.CreatedAt.strftime("%d %b %Y")
                    if item.CreatedAt
                    else None
                ),
                "author": item.author.Username if item.author else "Unknown",
            }
        )
    return jsonify(pending_data), 200


@content_bp.patch("/admin/content/<int:content_id>/status")
@jwt_required()
def update_content_status(content_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Bulletproof admin check
    is_admin = getattr(user, "is_admin", False)
    if not is_admin and hasattr(user, "Role") and user.Role:
        is_admin = user.Role.lower() == "admin"

    if not user or not is_admin:
        return jsonify({"error": "Access forbidden: Admin privileges required"}), 403

    data = request.get_json() or {}
    new_status = data.get("status")
    reason = data.get("reason", "").strip()

    if new_status not in ["Published", "Rejected", "Pending"]:
        return jsonify({"error": "Invalid status value"}), 400

    content = Content.query.get_or_404(content_id)
    content.Status = new_status

    if new_status == "Published":
        content.IsApproved = True
        content.RejectionReason = None
        notif_msg = (
            f"Your submission '{content.Title}' has been approved and published!"
        )
    else:
        content.IsApproved = False
        content.RejectionReason = (
            reason if reason else "No specific reason provided."
        )
        notif_msg = f"Your submission '{content.Title}' was rejected. Reason: {content.RejectionReason}"

    new_notif = Notification(
        UserID=content.UserID,
        ContentID=content.ContentID,
        Message=notif_msg,
        IsRead=False,
    )
    db.session.add(new_notif)
    db.session.commit()

    return (
        jsonify({"message": f"Content successfully marked as {new_status}"}),
        200,
    )


@content_bp.delete("/admin/content/<int:content_id>")
@jwt_required()
def delete_content(content_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    # Bulletproof admin check
    is_admin = getattr(user, "is_admin", False)
    if not is_admin and hasattr(user, "Role") and user.Role:
        is_admin = user.Role.lower() == "admin"

    if not user or not is_admin:
        return jsonify({"error": "Access forbidden: Admin privileges required"}), 403

    content = Content.query.get_or_404(content_id)

    # Remove foreign key references before deleting post
    Notification.query.filter_by(ContentID=content_id).delete()

    db.session.delete(content)
    db.session.commit()

    return jsonify({"message": "Content deleted successfully"}), 200