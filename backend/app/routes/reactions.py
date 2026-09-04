from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request

from app.extensions import db
from app.models import Content, ContentReaction, User, normalized_role


reactions_bp = Blueprint("reactions", __name__)


def _summary(content_id, user_id=None):
    reactions = ContentReaction.query.filter_by(ContentID=content_id).all()
    return {
        "likes": sum(reaction.Reaction == "like" for reaction in reactions),
        "dislikes": sum(reaction.Reaction == "dislike" for reaction in reactions),
        "userReaction": next(
            (reaction.Reaction for reaction in reactions if reaction.UserID == user_id),
            None,
        ),
    }


def _visible_content(content_id):
    content = db.session.get(Content, content_id)
    if not content:
        return None, False, None

    verify_jwt_in_request(optional=True)
    identity = get_jwt_identity()
    user = db.session.get(User, int(identity)) if identity is not None else None
    is_public = content.Status == "Published" and content.IsApproved
    can_view_private = user and (
        user.UserID == content.UserID
        or normalized_role(user.Role) in {"admin", "tech_writer"}
    )
    return content, bool(is_public or can_view_private), user


@reactions_bp.get("/content/<int:content_id>/reactions")
def reaction_summary(content_id):
    content, can_view, user = _visible_content(content_id)
    if not content or not can_view:
        return jsonify({"error": "Content not found"}), 404
    return jsonify(_summary(content_id, user.UserID if user else None)), 200


@reactions_bp.post("/content/<int:content_id>/reactions")
@jwt_required()
def react_to_content(content_id):
    content, can_view, _user = _visible_content(content_id)
    if not content or not can_view:
        return jsonify({"error": "Content not found"}), 404
    data = request.get_json(silent=True) or {}
    reaction_type = data.get("type")
    if reaction_type not in ("like", "dislike"):
        return jsonify({"error": "type must be 'like' or 'dislike'"}), 400

    user_id = int(get_jwt_identity())
    existing = ContentReaction.query.filter_by(UserID=user_id, ContentID=content_id).first()
    if existing and existing.Reaction == reaction_type:
        db.session.delete(existing)
    elif existing:
        existing.Reaction = reaction_type
    else:
        db.session.add(
            ContentReaction(UserID=user_id, ContentID=content_id, Reaction=reaction_type)
        )
    db.session.commit()

    like_count = ContentReaction.query.filter_by(
        ContentID=content_id, Reaction="like"
    ).count()
    content = db.session.get(Content, content_id)
    content.LikesCount = like_count
    db.session.commit()
    return jsonify(_summary(content_id, user_id)), 200
