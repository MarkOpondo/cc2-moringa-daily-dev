from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Content, Share, User, Wishlist
from app.serializers import serialize_content


interactions_bp = Blueprint("interactions", __name__)


@interactions_bp.get("/wishlist")
@jwt_required()
def get_wishlist():
    items = (
        Wishlist.query.join(Content)
        .filter(
            Wishlist.UserID == int(get_jwt_identity()),
            Content.Status == "Published",
            Content.IsApproved.is_(True),
        )
        .all()
    )
    return jsonify([serialize_content(item.content, include_private=False) for item in items]), 200


@interactions_bp.post("/wishlist")
@jwt_required()
def add_to_wishlist():
    data = request.get_json(silent=True) or {}
    content_id = data.get("contentId", data.get("content_id"))
    if not content_id:
        return jsonify({"error": "contentId is required"}), 400
    content = db.session.get(Content, content_id)
    if not content or content.Status != "Published" or not content.IsApproved:
        return jsonify({"error": "Published content not found"}), 404

    existing = Wishlist.query.filter_by(
        UserID=int(get_jwt_identity()), ContentID=content_id
    ).first()
    if existing:
        return jsonify({"error": "Already in wishlist"}), 409

    item = Wishlist(UserID=int(get_jwt_identity()), ContentID=content_id)
    db.session.add(item)
    db.session.commit()
    return jsonify({"id": item.WishlistID, "contentId": item.ContentID}), 201


@interactions_bp.delete("/wishlist/<int:content_id>")
@jwt_required()
def remove_from_wishlist(content_id):
    item = Wishlist.query.filter_by(
        ContentID=content_id, UserID=int(get_jwt_identity())
    ).first()
    if not item:
        return jsonify({"error": "Wishlist item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Removed from wishlist"}), 200


@interactions_bp.post("/content/<int:content_id>/share")
@jwt_required()
def share_content(content_id):
    data = request.get_json(silent=True) or {}
    recipient_id = data.get("sharedWithUserId", data.get("shared_with_user_id"))
    content = db.session.get(Content, content_id)
    recipient = db.session.get(User, recipient_id) if recipient_id else None
    if not content or content.Status != "Published" or not content.IsApproved:
        return jsonify({"error": "Published content not found"}), 404
    if not recipient or not recipient.IsActive:
        return jsonify({"error": "Active recipient not found"}), 404

    share = Share(
        UserID=int(get_jwt_identity()),
        ContentID=content_id,
        SharedWithUserID=recipient.UserID,
    )
    db.session.add(share)
    db.session.commit()
    return jsonify({"id": share.ShareID, "message": "Content shared"}), 201
