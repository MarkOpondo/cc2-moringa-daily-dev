from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import Category, Content
from . import content_bp

try:
    from app.models import Reaction
except ImportError:
    Reaction = None


@content_bp.get("/categories")
def get_categories():
    categories = Category.query.all()
    return (
        jsonify([
            {
                "id": c.CategoryID,
                "name": c.Name,
                "description": c.Description,
            }
            for c in categories
        ]),
        200,
    )


@content_bp.get("/content")
@jwt_required(optional=True)
def get_content_feed():
    current_user_id = get_jwt_identity()
    param_value = request.args.get("category")
    query = Content.query.filter_by(Status="Published")

    if param_value and param_value.lower() != "all":
        if param_value.lower() in [
            "articles",
            "videos",
            "podcasts",
            "article",
            "video",
            "podcast",
        ]:
            content_type_val = param_value.rstrip("s").lower()
            query = query.filter(Content.ContentType.ilike(f"%{content_type_val}%"))
        else:
            query = query.join(Content.categories).filter(
                Category.Name.ilike(param_value)
            )

    contents = query.order_by(Content.CreatedAt.desc()).all()

    feed_data = []
    for item in contents:
        if hasattr(item, "LikesCount") and item.LikesCount is not None:
            likes_count = item.LikesCount
        elif hasattr(item, "likes_count") and item.likes_count is not None:
            likes_count = item.likes_count
        elif hasattr(item, "reactions") and item.reactions is not None:
            likes_count = len(item.reactions)
        else:
            likes_count = 0

        is_liked = False
        if current_user_id and Reaction:
            user_reaction = Reaction.query.filter_by(
                ContentID=item.ContentID, UserID=current_user_id
            ).first()
            is_liked = user_reaction is not None

        comments_count = len(item.comments) if hasattr(item, "comments") else 0
        formatted_date = (
            item.CreatedAt.strftime("%d %b %Y") if item.CreatedAt else None
        )

        feed_data.append({
            # Snake_case keys (Python standard)
            "content_id": item.ContentID,
            "content_type": item.ContentType,
            "content_url": item.ContentURL,
            "views_count": item.ViewsCount,
            "likes_count": likes_count,
            "is_liked": is_liked,
            "comments_count": comments_count,
            "created_at": formatted_date,
            # CamelCase keys (JavaScript/React standard)
            "contentId": item.ContentID,
            "contentType": item.ContentType,
            "contentUrl": item.ContentURL,
            "viewsCount": item.ViewsCount,
            "likesCount": likes_count,
            "isLiked": is_liked,
            "commentsCount": comments_count,
            "createdAt": formatted_date,
            # Shared fields
            "title": item.Title,
            "description": item.Description,
            "duration": item.Duration,
            "hashtags": item.Hashtags,
            "status": item.Status,
            "author": {
                "username": item.author.Username if item.author else None,
                "profile_image": item.author.profile.ProfileImage
                if item.author and item.author.profile
                else None,
            },
            "categories": [
                {"id": cat.CategoryID, "name": cat.Name} for cat in item.categories
            ],
        })

    return jsonify(feed_data), 200