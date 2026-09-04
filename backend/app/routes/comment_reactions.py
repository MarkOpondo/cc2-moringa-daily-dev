from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Comment, CommentReaction


comment_reactions_bp = Blueprint("comment_reactions", __name__)


def _summary(comment_id, user_id):
    reactions = CommentReaction.query.filter_by(CommentID=comment_id).all()
    return {
        "likes": sum(reaction.Reaction == "like" for reaction in reactions),
        "dislikes": sum(reaction.Reaction == "dislike" for reaction in reactions),
        "userReaction": next(
            (reaction.Reaction for reaction in reactions if reaction.UserID == user_id),
            None,
        ),
    }


@comment_reactions_bp.post("/comments/<int:comment_id>/reactions")
@jwt_required()
def react_to_comment(comment_id):
    data = request.get_json(silent=True) or {}
    reaction_type = data.get("type")
    if reaction_type not in ("like", "dislike"):
        return jsonify({"error": "type must be 'like' or 'dislike'"}), 400
    if not db.session.get(Comment, comment_id):
        return jsonify({"error": "Comment not found"}), 404

    user_id = int(get_jwt_identity())
    existing = CommentReaction.query.filter_by(UserID=user_id, CommentID=comment_id).first()
    if existing and existing.Reaction == reaction_type:
        db.session.delete(existing)
    elif existing:
        existing.Reaction = reaction_type
    else:
        db.session.add(CommentReaction(UserID=user_id, CommentID=comment_id, Reaction=reaction_type))
    db.session.commit()
    return jsonify(_summary(comment_id, user_id)), 200


@comment_reactions_bp.delete("/comments/<int:comment_id>/reactions")
@jwt_required()
def remove_comment_reaction(comment_id):
    user_id = int(get_jwt_identity())
    reaction = CommentReaction.query.filter_by(UserID=user_id, CommentID=comment_id).first()
    if not reaction:
        return jsonify({"error": "Reaction not found"}), 404
    db.session.delete(reaction)
    db.session.commit()
    return jsonify(_summary(comment_id, user_id)), 200
