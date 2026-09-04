from app.models import Comment, Content, User, normalized_role


def iso(value):
    return value.isoformat() if value else None


def serialize_user(user: User | None, include_email=True):
    if not user:
        return None

    profile = user.profile
    payload = {
        "id": user.UserID,
        "username": user.Username,
        "role": normalized_role(user.Role),
        "isActive": bool(user.IsActive),
        "profileImage": profile.ProfileImage if profile else None,
    }
    if include_email:
        payload["email"] = user.Email
    return payload


def serialize_category(category):
    return {
        "id": category.CategoryID,
        "name": category.Name,
        "description": category.Description,
    }


def serialize_content(content: Content, include_private=True):
    likes = sum(1 for reaction in content.reactions if reaction.Reaction == "like")
    dislikes = sum(1 for reaction in content.reactions if reaction.Reaction == "dislike")
    categories = [serialize_category(category) for category in content.categories]

    data = {
        "id": content.ContentID,
        "title": content.Title,
        "body": content.Description or "",
        "type": (content.ContentType or "article").lower(),
        "mediaUrl": content.ContentURL,
        "status": (content.Status or "draft").lower(),
        "isApproved": bool(content.IsApproved),
        "createdAt": iso(content.CreatedAt),
        "updatedAt": iso(content.UpdatedAt),
        "author": serialize_user(content.author, include_email=False),
        "categories": categories,
        "likesCount": likes,
        "dislikesCount": dislikes,
        "commentsCount": len(content.comments),
        "viewsCount": content.ViewsCount or 0,
        "duration": content.Duration,
        "summary": content.Summary,
        "thumbnailUrl": content.ThumbnailURL,
        "hashtags": content.Hashtags,
    }

    if include_private:
        data["authorId"] = content.UserID
        data["rejectionReason"] = content.RejectionReason

    return data


def serialize_comment(comment: Comment):
    return {
        "id": comment.CommentID,
        "body": comment.Text,
        "parentId": comment.ParentCommentID,
        "createdAt": iso(comment.CreatedAt),
        "updatedAt": iso(comment.UpdatedAt),
        "author": serialize_user(comment.author, include_email=False),
        "replies": [serialize_comment(reply) for reply in comment.replies],
    }
