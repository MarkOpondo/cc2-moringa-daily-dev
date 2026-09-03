import os

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from app.extensions import db
from app.models import Content, User, Category, Subscription, Notification, ContentReaction
from app.utils import role_required

content_bp = Blueprint("content", __name__)


def safe_get_user_id():
    """Extract integer user ID safely from JWT identity."""
    identity = get_jwt_identity()
    if not identity:
        return None
    if isinstance(identity, dict):
        return int(identity.get("id"))
    return int(identity)


def _notify_subscribers(content_item):
    """Send notifications to users subscribed to this content's categories.

    Never raises: a notification problem must not fail the API request that
    triggered it.
    """
    try:
        notifications = []

        for category in content_item.categories:
            subscriptions = Subscription.query.filter_by(
                CategoryID=category.CategoryID
            ).all()

            for sub in subscriptions:
                if sub.UserID != content_item.UserID:
                    notifications.append(
                        Notification(
                            UserID=sub.UserID,
                            ContentID=content_item.ContentID,
                            Message=(
                                f"New content in your feed: "
                                f"'{content_item.Title}'"
                            ),
                        )
                    )

        if notifications:
            db.session.add_all(notifications)
            db.session.commit()
    except Exception:
        db.session.rollback()


# -------------------------------------------------------------------
# 1. LIST CONTENT (WITH PAGINATION)
# -------------------------------------------------------------------
DEFAULT_AVATAR = "https://ui-avatars.com/api/?background=random&name="
DEFAULT_COVER = "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=600&auto=format&fit=crop"


def _absolute_media_url(url, request_host=None):
    """Turn a relative /static/uploads/... path into an absolute URL."""
    if not url:
        return None
    if url.startswith("http"):
        return url
    base = request_host or f"http://127.0.0.1:5001"
    return f"{base}{url}"


def _serialize_content(content, current_user_id=None):
    """Common serializer so list & detail return the same shape."""
    author_username = content.author.Username if getattr(content, "author", None) else "Anonymous"

    profile_img = None
    if getattr(content, "author", None) and getattr(content.author, "profile", None):
        profile_img = getattr(content.author.profile, "ProfileImage", None)
    if not profile_img:
        profile_img = f"{DEFAULT_AVATAR}{author_username}"
    else:
        profile_img = _absolute_media_url(profile_img)

    content_img = _absolute_media_url(content.ContentURL) or DEFAULT_COVER
    thumbnail = _absolute_media_url(getattr(content, "ThumbnailURL", None))

    likes_count = (
        ContentReaction.query.filter_by(
            ContentID=content.ContentID, Reaction="like"
        ).count()
    )
    dislikes_count = (
        ContentReaction.query.filter_by(
            ContentID=content.ContentID, Reaction="dislike"
        ).count()
    )

    is_liked = False
    if current_user_id:
        reaction = ContentReaction.query.filter_by(
            ContentID=content.ContentID, UserID=current_user_id
        ).first()
        is_liked = bool(reaction and reaction.Reaction == "like")

    categories = [
        {"id": cat.CategoryID, "name": cat.Name}
        for cat in content.categories
    ]
    category = categories[0] if categories else None

    return {
        "id": content.ContentID,
        "content_id": content.ContentID,
        "title": content.Title,
        "description": content.Description,
        "summary": getattr(content, "Summary", None),
        "type": content.ContentType,
        "content_type": content.ContentType,
        "url": content.ContentURL,
        "content_url": content.ContentURL,
        "thumbnail": thumbnail,
        "thumbnail_url": thumbnail,
        "content_image": content_img,
        "status": content.Status,
        "is_approved": getattr(content, "IsApproved", False),
        "duration": getattr(content, "Duration", None),
        "author_id": content.UserID,
        "author": {
            "username": author_username,
            "profile_image": profile_img
        },
        "views_count": getattr(content, "ViewsCount", 0) or 0,
        "likes_count": likes_count,
        "dislikes_count": dislikes_count,
        "is_liked": is_liked,
        "comments_count": len(content.comments) if hasattr(content, "comments") else 0,
        "categories": categories,
        "category": category,
        "created_at": content.CreatedAt.isoformat() if content.CreatedAt else None,
    }


@content_bp.route("", methods=["GET"], strict_slashes=False)
@content_bp.route("/", methods=["GET"], strict_slashes=False)
@jwt_required(optional=True)
def list_content():
    # Capture Pagination Query Params
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # Capture Filter Params
    category_id = request.args.get("category_id", type=int)
    category_name = request.args.get("category")
    status = request.args.get("status", "Published")
    content_type = request.args.get("type")
    search = (request.args.get("search") or request.args.get("q") or "").strip()

    try:
        current_user_id = safe_get_user_id()
    except Exception:
        current_user_id = None

    query = Content.query

    # 1. Filter Category
    if category_id:
        query = query.filter(Content.categories.any(Category.CategoryID == category_id))
    elif category_name and category_name.lower() != "all":
        if category_name.isdigit():
            query = query.filter(Content.categories.any(Category.CategoryID == int(category_name)))
        else:
            query = query.filter(Content.categories.any(Category.Name.ilike(f"%{category_name.strip()}%")))

    # 2. Filter Content Type (case-insensitive)
    if content_type:
        query = query.filter(Content.ContentType.ilike(f"%{content_type}%"))

    # 3. Filter Status (case-insensitive so "pending" matches "Pending")
    if status and status.lower() != "all":
        query = query.filter(Content.Status.ilike(status))

    # 4. Simple text search on title/description
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                Content.Title.ilike(like),
                Content.Description.ilike(like),
            )
        )

    # 5. Apply Pagination
    paginated_query = query.order_by(Content.CreatedAt.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    items_data = [
        _serialize_content(content, current_user_id)
        for content in paginated_query.items
    ]

    return jsonify({
        "items": items_data,
        "pagination": {
            "total_items": paginated_query.total,
            "total_pages": paginated_query.pages,
            "current_page": paginated_query.page,
            "per_page": paginated_query.per_page,
            "has_next": paginated_query.has_next,
            "has_prev": paginated_query.has_prev
        }
    }), 200

# -------------------------------------------------------------------
# 2. GET SINGLE CONTENT
# -------------------------------------------------------------------
@content_bp.get("/<int:content_id>")
def get_single_content(content_id):
    item = db.session.get(Content, content_id)
    if not item:
        return jsonify({"error": "Content not found"}), 404

    # NOTE: the response is returned for every item, whether or not it has
    # an author record (the old version only returned inside the author
    # check, which made author-less content 500).
    return jsonify(_serialize_content(item)), 200

# -------------------------------------------------------------------
# 3. CREATE CONTENT
# -------------------------------------------------------------------
@content_bp.route("", methods=["POST"], strict_slashes=False)
@jwt_required()
def create_content():
    try:
        user_id = safe_get_user_id()

        if not user_id:
            return jsonify({"error": "Unauthorized user"}), 401

        user = db.session.get(User, user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Handle JSON or multipart/form-data
        if request.is_json:
            data = request.get_json(silent=True) or {}
            file = None
            thumbnail_file = None
        else:
            data = request.form.to_dict()
            file = (
                request.files.get("file")
                or request.files.get("media_file")
                or request.files.get("media")
                or request.files.get("content_url")
            )
            thumbnail_file = (
                request.files.get("thumbnail")
                or request.files.get("thumbnail_file")
            )

        title = data.get("title") or data.get("Title")

        description = (
            data.get("description")
            or data.get("Description")
            or data.get("body")
            or ""
        )

        content_type = (
            data.get("content_type")
            or data.get("type")
            or "Article"
        )

        content_type = str(content_type).capitalize()

        allowed_types = ["Article", "Video", "Audio", "Image"]

        if content_type not in allowed_types:
            return jsonify({
                "error": (
                    "Invalid Content type. Must be one of: "
                    + ", ".join(allowed_types)
                )
            }), 400

        category_id = (
            data.get("category_id")
            or data.get("categoryId")
            or data.get("category")
        )

        if not title:
            return jsonify({"error": "Title is required"}), 400

        # -----------------------------------------------------------
        # File / URL handling
        # -----------------------------------------------------------

        def _save_upload(upload_file):
            filename = secure_filename(upload_file.filename)
            if not filename:
                return None
            upload_dir = current_app.config.get(
                "UPLOAD_FOLDER",
                "static/uploads"
            )
            os.makedirs(upload_dir, exist_ok=True)
            save_path = os.path.join(upload_dir, filename)
            upload_file.save(save_path)
            return f"/static/uploads/{filename}"

        file_url = data.get("content_url") or data.get("url") or ""

        if file:
            saved = _save_upload(file)
            if saved:
                file_url = saved

        thumbnail_url = data.get("thumbnail_url") or ""

        if thumbnail_file:
            saved_thumb = _save_upload(thumbnail_file)
            if saved_thumb:
                thumbnail_url = saved_thumb

        # -----------------------------------------------------------
        # Status / approval logic
        # -----------------------------------------------------------

        role = getattr(user, "Role", "user") or "user"

        if role.lower() in ["admin", "tech_writer"]:
            status = "Published"
            is_approved = True
        else:
            status = "Pending"
            is_approved = False

        # -----------------------------------------------------------
        # Create content
        # -----------------------------------------------------------

        new_content = Content(
            UserID=user_id,
            Title=title,
            Description=description,
            ContentType=content_type,
            ContentURL=file_url,
            ThumbnailURL=thumbnail_url or None,
            Status=status,
            IsApproved=is_approved,
            Summary=data.get("summary") or None,
            Duration=data.get("duration") or data.get("read_time") or None,
        )

        # -----------------------------------------------------------
        # Category association
        # -----------------------------------------------------------

        if category_id:
            try:
                category = db.session.get(
                    Category,
                    int(category_id)
                )

                if not category:
                    return jsonify({
                        "error": "Category not found"
                    }), 404

                new_content.categories.append(category)

            except (ValueError, TypeError):
                return jsonify({
                    "error": "Invalid Category ID format"
                }), 400

        db.session.add(new_content)
        db.session.commit()

        # Notify category subscribers when content goes live immediately
        # (Pending content notifies on admin approval instead).
        if status == "Published":
            _notify_subscribers(new_content)

        return jsonify({
            "message": "Content submitted successfully!",
            "id": new_content.ContentID,
            "content_id": new_content.ContentID,
            "status": new_content.Status,
            "is_approved": getattr(
                new_content,
                "IsApproved",
                False
            )
        }), 201

    except Exception as e:
        db.session.rollback()

        from app.schema_doctor import looks_like_schema_drift, schema_drift_hint

        details = str(e)
        error = "Failed to submit content"
        if looks_like_schema_drift(details):
            error = schema_drift_hint()

        return jsonify({
            "error": error,
            "details": details
        }), 500

# -------------------------------------------------------------------
# EDIT CONTENT (PUT/PATCH)
# -------------------------------------------------------------------
@content_bp.route("/<int:content_id>", methods=["PUT", "PATCH"],strict_slashes=False)
@jwt_required()
def edit_content(content_id):
    item = db.session.get(Content, content_id)
    if not item:
        return jsonify({"error": "Content not found"}), 404

    # 1. User Identity & Permission Check
    try:
        user_id = safe_get_user_id()
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid user identity"}), 400

    current_user = db.session.get(User, user_id)
    if not current_user:
        return jsonify({"error": "User not found"}), 404

    # Authorize: Only the author or an Admin can edit
    if item.UserID != current_user.UserID and str(current_user.Role).lower() != "admin":
        return jsonify({"error": "Forbidden: Cannot edit another user's content"}), 403

    # 2. Extract Body (JSON or Form Data)
    if request.is_json:
        data = request.get_json() or {}
        file = None
    else:
        data = request.form.to_dict()
        file = (
            request.files.get("file")
            or request.files.get("media_file")
            or request.files.get("media")
            or request.files.get("content_url")
        )

    # 3. Content Type Validation (if provided)
    raw_type = data.get("type") or data.get("content_type")
    if raw_type:
        formatted_type = str(raw_type).capitalize()
        allowed_types = ["Article", "Video", "Audio", "Image"]
        if formatted_type not in allowed_types:
            return jsonify({"error": f"Invalid Content type. Must be one of: {', '.join(allowed_types)}"}), 400
        item.ContentType = formatted_type

    # 4. Handle Optional File Re-upload
    if file:
        filename = secure_filename(file.filename)
        upload_dir = current_app.config.get("UPLOAD_FOLDER", "static/uploads")
        os.makedirs(upload_dir, exist_ok=True)
        save_path = os.path.join(upload_dir, filename)
        file.save(save_path)
        item.ContentURL = f"/static/uploads/{filename}"
    elif "url" in data or "content_url" in data:
        item.ContentURL = data.get("url") or data.get("content_url")

    # 5. Update Status Constraint Compliance
    if "status" in data:
        req_status = str(data.get("status")).capitalize()
        if req_status in ["Draft", "Pending", "Published", "Archived"]:
            item.Status = req_status

    # 6. Basic Fields Update
    if "title" in data or "Title" in data:
        item.Title = data.get("title") or data.get("Title")
    if "description" in data or "Description" in data or "body" in data:
        item.Description = data.get("description") or data.get("Description") or data.get("body")
    if "summary" in data:
        item.Summary = data.get("summary")
    if "duration" in data:
        item.Duration = data.get("duration")

    # 7. Category Association Update
    category_id = data.get("category_id") or data.get("category") or data.get("categoryId")
    if category_id:
        try:
            category = db.session.get(Category, int(category_id))
            if not category:
                return jsonify({"error": "Category not found"}), 404
            item.categories = [category]
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid Category ID format"}), 400

    # 8. Save Changes
    try:
        db.session.commit()
        return jsonify({
            "message": "Content updated successfully.",
            "content": {
                "id": item.ContentID,
                "title": item.Title,
                "content_type": item.ContentType,
                "status": item.Status,
                "content_url": item.ContentURL
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update content", "details": str(e)}), 500


# -------------------------------------------------------------------
# DELETE CONTENT
# -------------------------------------------------------------------
@content_bp.delete("/<int:content_id>",strict_slashes=False)
@jwt_required()
def delete_content(content_id):
    item = db.session.get(Content, content_id)
    if not item:
        return jsonify({"error": "Content not found"}), 404

    # 1. User Identity Check
    try:
        user_id = safe_get_user_id()
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid user identity"}), 400

    current_user = db.session.get(User, user_id)
    if not current_user:
        return jsonify({"error": "User not found"}), 404

    # 2. Authorization Check (Author or Admin only)
    if item.UserID != current_user.UserID and str(current_user.Role).lower() != "admin":
        return jsonify({"error": "Forbidden: Cannot delete this item"}), 403

    # 3. Database Deletion
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({
            "message": "Content deleted successfully.",
            "content_id": content_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to delete content", "details": str(e)}), 500

# -------------------------------------------------------------------
# FLAG CONTENT
# -------------------------------------------------------------------
@content_bp.route("/<int:content_id>/flag", methods=["PATCH"], strict_slashes=False)
@jwt_required()
@role_required("Admin", "tech_writer")
def flag_content(content_id):
    item = db.session.get(Content, content_id)
    if not item:
        return jsonify({"error": "Content not found"}), 404

    try:
        # Mark as unapproved
        if hasattr(item, "IsApproved"):
            item.IsApproved = False

        # Set status to Archived to keep compliance with Status CheckConstraints
        # ('Draft', 'Pending', 'Published', 'Archived')
        item.Status = "Archived"

        db.session.commit()

        return jsonify({
            "message": "Content flagged and archived successfully.",
            "content_id": content_id,
            "status": item.Status,
            "is_approved": getattr(item, "IsApproved", False)
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to flag content", "details": str(e)}), 500
