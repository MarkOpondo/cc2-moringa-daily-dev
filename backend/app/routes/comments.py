from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request

from app.extensions import db
from app.models import Comment, Content, User, normalized_role
from app.serializers import serialize_comment


comments_bp = Blueprint("comments", __name__)


def _current_user():
    return db.session.get(User, int(get_jwt_identity()))


def _comment_payload(comment):
    return serialize_comment(comment)


@comments_bp.get("/content/<int:content_id>/comments")
def get_comments(content_id):
    content = db.session.get(Content, content_id)
    if not content:
        return jsonify({"error": "Content not found"}), 404

    verify_jwt_in_request(optional=True)
    identity = get_jwt_identity()
    viewer = db.session.get(User, int(identity)) if identity is not None else None
    is_public = content.Status == "Published" and content.IsApproved
    can_view_private = viewer and (
        viewer.UserID == content.UserID or normalized_role(viewer.Role) in {"admin", "tech_writer"}
    )
    if not is_public and not can_view_private:
        return jsonify({"error": "Content not found"}), 404

    comments = Comment.query.filter_by(
        ContentID=content_id, ParentCommentID=None
    ).order_by(Comment.CreatedAt.asc()).all()
    return jsonify([_comment_payload(comment) for comment in comments]), 200


@comments_bp.post("/content/<int:content_id>/comments")
@jwt_required()
def add_comment(content_id):
    user = _current_user()
    data = request.get_json(silent=True) or {}
    body = str(data.get("body") or "").strip()
    parent_id = data.get("parentId", data.get("parent_comment_id"))

    content = db.session.get(Content, content_id)
    if not user or not user.IsActive:
        return jsonify({"error": "Active user account required"}), 403
    if not content or content.Status != "Published" or not content.IsApproved:
        return jsonify({"error": "Published content not found"}), 404
    if not body:
        return jsonify({"error": "Comment body is required"}), 400

    parent = None
    if parent_id is not None:
        try:
            parent = db.session.get(Comment, int(parent_id))
        except (TypeError, ValueError):
            parent = None
        if not parent or parent.ContentID != content_id:
            return jsonify({"error": "Parent comment not found for this content"}), 400

    comment = Comment(
        Text=body,
        ContentID=content_id,
        UserID=user.UserID,
        ParentCommentID=parent.CommentID if parent else None,
    )
    db.session.add(comment)
    db.session.commit()
    return jsonify(_comment_payload(comment)), 201


@comments_bp.patch("/comments/<int:comment_id>")
@jwt_required()
def edit_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    user = _current_user()
    if not comment:
        return jsonify({"error": "Comment not found"}), 404
    if not user or (comment.UserID != user.UserID and normalized_role(user.Role) != "admin"):
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json(silent=True) or {}
    body = str(data.get("body") or "").strip()
    if not body:
        return jsonify({"error": "Comment body is required"}), 400
    comment.Text = body
    db.session.commit()
    return jsonify(_comment_payload(comment)), 200


@comments_bp.delete("/comments/<int:comment_id>")
@jwt_required()
def delete_comment(comment_id):
    comment = db.session.get(Comment, comment_id)
    user = _current_user()
    if not comment:
        return jsonify({"error": "Comment not found"}), 404
    if not user or (comment.UserID != user.UserID and normalized_role(user.Role) != "admin"):
        return jsonify({"error": "Forbidden"}), 403

    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted"}), 200
