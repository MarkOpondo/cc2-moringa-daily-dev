from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.models import Comment
from . import content_bp


@content_bp.get("/content/<int:content_id>/comments")
def get_comments(content_id):
    comments = (
        Comment.query.filter_by(ContentID=content_id, ParentCommentID=None)
        .order_by(Comment.CreatedAt.desc())
        .all()
    )

    comments_data = []
    for comment in comments:
        comments_data.append(
            {
                "comment_id": comment.CommentID,
                "content_id": comment.ContentID,
                "text": comment.Text,
                "parent_comment_id": comment.ParentCommentID,
                "created_at": (
                    comment.CreatedAt.strftime("%d %b %Y %H:%M")
                    if comment.CreatedAt
                    else None
                ),
                "user": {
                    "username": (
                        comment.author.Username if comment.author else None
                    ),
                    "profile_image": (
                        comment.author.profile.ProfileImage
                        if comment.author and comment.author.profile
                        else None
                    ),
                },
                "replies": [
                    {
                        "comment_id": reply.CommentID,
                        "content_id": reply.ContentID,
                        "text": reply.Text,
                        "parent_comment_id": reply.ParentCommentID,
                        "created_at": (
                            reply.CreatedAt.strftime("%d %b %Y %H:%M")
                            if reply.CreatedAt
                            else None
                        ),
                        "user": {
                            "username": (
                                reply.author.Username if reply.author else None
                            ),
                            "profile_image": (
                                reply.author.profile.ProfileImage
                                if reply.author and reply.author.profile
                                else None
                            ),
                        },
                    }
                    for reply in comment.replies
                ],
            }
        )

    return jsonify(comments_data), 200


@content_bp.post("/content/<int:content_id>/comments")
@jwt_required()
def create_comment(content_id):
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}

    text = data.get("text") or data.get("body")
    parent_comment_id = data.get("parent_comment_id")

    if not text:
        return jsonify({"error": "Comment text is required"}), 400

    new_comment = Comment(
        ContentID=content_id,
        UserID=current_user_id,
        Text=text,
        ParentCommentID=parent_comment_id,
    )

    db.session.add(new_comment)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Comment added successfully",
                "comment_id": new_comment.CommentID,
                "text": new_comment.Text,
                "parent_comment_id": new_comment.ParentCommentID,
                "created_at": (
                    new_comment.CreatedAt.strftime("%d %b %Y %H:%M")
                    if new_comment.CreatedAt
                    else None
                ),
                "user": {
                    "username": (
                        new_comment.author.Username
                        if new_comment.author
                        else None
                    ),
                    "profile_image": (
                        new_comment.author.profile.ProfileImage
                        if new_comment.author and new_comment.author.profile
                        else None
                    ),
                },
            }
        ),
        201,
    )