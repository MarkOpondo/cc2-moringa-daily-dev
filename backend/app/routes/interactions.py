from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import ContentReaction, Share, Wishlist

interactions_bp = Blueprint("interactions", __name__)

#============================== REACTIONS ==============================

# GET REACTIONS FOR CONTENT (PUBLIC)
@interactions_bp.get("/content/<int:content_id>/reactions")
def get_content_reactions(content_id):
    reactions = ContentReaction.query.filter_by(ContentID=content_id).all()
    return jsonify([
        {
            "id": getattr(r, "ReactionID", getattr(r, "id", None)),
            "user_id": r.UserID,
            "type": r.Reaction
        } for r in reactions
    ]), 200


# REACT TO CONTENT
@interactions_bp.post("/content/<int:content_id>/reactions")
@jwt_required()
def react_to_content(content_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    reaction_type = data.get("type")
    
    if reaction_type not in ("like", "dislike", "Like", "Love", "Haha", "Wow"):
        return jsonify({"error": "Invalid reaction type."}), 400

    user_id = int(get_jwt_identity())

    existing = ContentReaction.query.filter_by(
        UserID=user_id,
        ContentID=content_id
    ).first()

    if existing: 
        existing.Reaction = reaction_type
    else:
        reaction = ContentReaction(
            UserID=user_id,
            ContentID=content_id,
            Reaction=reaction_type
        )
        db.session.add(reaction)

    db.session.commit()
    return jsonify({"message": "Reaction recorded."}), 200


#=================================== SHARE ==============================
@interactions_bp.post("/content/<int:content_id>/share")
@jwt_required()
def share_content(content_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided."}), 400

    shared_with_user_id = data.get("shared_with_user_id")

    if not shared_with_user_id:
        return jsonify({"error": "shared_with_user_id is required."}), 400
    
    share = Share(
        UserID=int(get_jwt_identity()),
        ContentID=content_id,
        SharedWithUserID=shared_with_user_id
    )       
    db.session.add(share)    
    db.session.commit()

    return jsonify({"message": "Share recorded."}), 200


#=================================== WISHLIST ==============================
@interactions_bp.get("/users/me/wishlist")
@jwt_required()
def get_wishlist():
    user_id = int(get_jwt_identity())

    items = Wishlist.query.filter_by(UserID=user_id).all()
    
    return jsonify([{
        "id": wishlist.WishlistID,
        "content_id": wishlist.ContentID
    } for wishlist in items]), 200


@interactions_bp.post("/wishlist")
@jwt_required()
def add_to_wishlist():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    content_id = data.get("content_id")

    if not content_id:
        return jsonify({"error": "content_id is required"}), 400
    
    user_id = int(get_jwt_identity())

    # Prevent duplicates
    existing = Wishlist.query.filter_by(
        UserID=user_id, ContentID=content_id
    ).first()

    if existing:
        return jsonify({"error": "Already in wishlist."}), 409

    wishlist = Wishlist(
        UserID=user_id,
        ContentID=content_id
    )    
    db.session.add(wishlist)
    db.session.commit()
    return jsonify({"message": "Added to wishlist."}), 201


@interactions_bp.delete("/wishlist/<int:wishlist_id>")
@jwt_required()
def remove_from_wishlist(wishlist_id):
    wishlist = Wishlist.query.get_or_404(wishlist_id)

    if wishlist.UserID != int(get_jwt_identity()):
        return jsonify({"error": "Forbidden"}), 403

    db.session.delete(wishlist)
    db.session.commit()
    return jsonify({"message": "Removed from wishlist."}), 200