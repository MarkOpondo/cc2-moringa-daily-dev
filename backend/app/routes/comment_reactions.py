from flask import Blueprint,request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import CommentReaction, Comment

comment_reactions_bp = Blueprint(
    "comment_reactions",__name__)

    #---------------------------- React to comment --------------------------
@comment_reactions_bp.post("/comments/<int:comment_id>/reactions")
@jwt_required()
def react_to_comment(comment_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No input data provided"
        }),400
    reaction_type=data.get("type")

    if reaction_type not in ("like", "dislike"):
        return jsonify({
            "error": "Reaction type must be 'like' or 'dislike'."
        }),400

    # Check that comment exists
    comment= Comment.query.get_or_404(comment_id)
    
    user_id=int(get_jwt_identity())
    # Check whether the user already reacted
    existing = CommentReaction.query.filter_by(
        UserID=user_id,
        CommentID= comment_id
    ).first()
    if existing:
        existing.Reaction = reaction_type
    else:
        reaction = CommentReaction(
            UserID=user_id,
            CommentID=comment_id,
            Reaction= reaction_type
        )    
        db.session.add(reaction)
    db.session.commit()
    return jsonify({
        "message": "Comment reaction recorded"
    }),200

#-------------------------------- REMOVE COMMENT REACTION ------------------------
@comment_reactions_bp.delete("/comments/<int:comment_id>/reactions")
@jwt_required()
def remove_comment_reaction(comment_id):
    user_id =int(get_jwt_identity())

    reaction = CommentReaction.query.filter_by(
        UserID=user_id,
        CommentID= comment_id
    ).first()
    if not reaction:
        return jsonify({
            "error": "Reaction not found"
        }),404
    db.session.delete(reaction)
    db.session.commit()
    return jsonify({
        "message": "Comment reaction removed"
    }),200        
