from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import db
from app.models import Content, Like, Notification, User
from . import content_bp


@content_bp.patch("/posts/<int:post_id>/like")
@jwt_required()
def toggle_like(post_id):
    content = Content.query.get_or_404(post_id)
    current_user_id = get_jwt_identity()

    # Convert JWT string ID to integer to match database UserID column type
    try:
        current_user_id = int(current_user_id)
    except (ValueError, TypeError):
        pass

    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json() or {}
    liked = data.get("liked", True)

    # 1. Handle adding or removing the user's like safely using the Like model
    existing_like = Like.query.filter_by(
        ContentID=post_id, UserID=current_user_id
    ).first()

    if liked and not existing_like:
        try:
            new_like = Like(ContentID=post_id, UserID=current_user_id)
            db.session.add(new_like)

            # Create a notification for the post author (skip if user likes their own post)
            if content.UserID != current_user_id:
                notification = Notification(
                    UserID=content.UserID,
                    ContentID=content.ContentID,
                    Message=f"{current_user.Username} liked your post: '{content.Title}'",
                )
                db.session.add(notification)

            db.session.commit()
        except Exception:
            db.session.rollback()  # Catches race conditions or unique constraint violations
    elif not liked and existing_like:
        db.session.delete(existing_like)

        # Create a notification for unliking
        if content.UserID != current_user_id:
            notification = Notification(
                UserID=content.UserID,
                ContentID=content.ContentID,
                Message=f"{current_user.Username} unliked your post: '{content.Title}'",
            )
            db.session.add(notification)

        db.session.commit()

    # 2. Derive the exact count directly from the dedicated likes table rows
    actual_likes_count = Like.query.filter_by(ContentID=post_id).count()

    # 3. Sync the count back to the Content model column
    if hasattr(content, "LikesCount"):
        content.LikesCount = actual_likes_count
        db.session.commit()
    elif hasattr(content, "likes_count"):
        content.likes_count = actual_likes_count
        db.session.commit()

    likes_count = actual_likes_count

    # 4. Verify exact like status for the current user
    user_like = Like.query.filter_by(
        ContentID=post_id, UserID=current_user_id
    ).first()
    is_liked = user_like is not None

    comments_count = len(content.comments) if hasattr(content, "comments") else 0
    formatted_date = (
        content.CreatedAt.strftime("%d %b %Y") if content.CreatedAt else None
    )

    return (
        jsonify(
            {
                # Snake_case keys
                "content_id": content.ContentID,
                "content_type": content.ContentType,
                "content_url": content.ContentURL,
                "views_count": content.ViewsCount,
                "likes_count": likes_count,
                "is_liked": is_liked,
                "comments_count": comments_count,
                "created_at": formatted_date,
                # CamelCase keys
                "contentId": content.ContentID,
                "contentType": content.ContentType,
                "contentUrl": content.ContentURL,
                "viewsCount": content.ViewsCount,
                "likesCount": likes_count,
                "isLiked": is_liked,
                "commentsCount": comments_count,
                "createdAt": formatted_date,
                # Shared fields
                "title": content.Title,
                "description": content.Description,
                "duration": content.Duration,
                "hashtags": content.Hashtags,
                "status": content.Status,
                "author": {
                    "username": (
                        content.author.Username if content.author else None
                    ),
                    "profile_image": (
                        content.author.profile.ProfileImage
                        if content.author and content.author.profile
                        else None
                    ),
                },
                "categories": [
                    {"id": cat.CategoryID, "name": cat.Name}
                    for cat in content.categories
                ],
            }
        ),
        200,
    )


@content_bp.get("/notifications")
@jwt_required()
def get_notifications():
    current_user_id = get_jwt_identity()
    try:
        current_user_id = int(current_user_id)
    except (ValueError, TypeError):
        pass

    # Fetch notifications for the logged-in user, newest first
    notifications = (
        Notification.query.filter_by(UserID=current_user_id)
        .order_by(Notification.NotificationID.desc())
        .all()
    )

    return (
        jsonify(
            [
                {
                    "id": n.NotificationID,
                    "message": n.Message,
                    "is_read": getattr(n, "IsRead", False),
                    "isRead": getattr(n, "IsRead", False),
                    "content_id": getattr(n, "ContentID", None),
                    "created_at": (
                        n.CreatedAt.strftime("%d %b %Y %H:%M")
                        if hasattr(n, "CreatedAt") and n.CreatedAt
                        else ""
                    ),
                }
                for n in notifications
            ]
        ),
        200,
    )