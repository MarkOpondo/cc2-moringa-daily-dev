from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Content, User, Category, Subscription, Notification
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
    """Send notifications to users subscribed to this content's categories."""
    notifications = []
    """Send notifications to users subscribed to this content's categories."""
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
                        UserID=sub.UserID,
                        ContentID=content_item.ContentID,
                        Message=f"New content in your feed: '{content_item.Title}'",
                    )
                )


    if notifications:
        db.session.add_all(notifications)
        db.session.commit()


# -------------------------------------------------------------------
# 1. LIST CONTENT
# -------------------------------------------------------------------
@content_bp.route("", methods=["GET"], strict_slashes=False)
@content_bp.route("/", methods=["GET"], strict_slashes=False)
@jwt_required(optional=True)
def list_content():
    category_id = request.args.get("category_id", type=int)
    category_name = request.args.get("category")
    status = request.args.get("status", "Published")
    content_type = request.args.get("type")

    query = Content.query

    # 1. Filter Category
    if category_id:
        query = query.filter(Content.categories.any(Category.CategoryID == category_id))
    elif category_name and category_name.lower() != "all":
        if category_name.isdigit():
            query = query.filter(Content.categories.any(Category.CategoryID == int(category_name)))
        else:
            query = query.filter(Content.categories.any(Category.Name.ilike(f"%{category_name.strip()}%")))

    # 2. Filter Content Type
    if content_type:
        query = query.filter(Content.ContentType.ilike(f"%{content_type}%"))

    # 3. Filter Status
    if status and status.lower() != "all":
        query = query.filter_by(Status=status)

    items = query.order_by(Content.CreatedAt.desc()).all()

    response = []
    for content in items:
        author_data = {"username": None, "profile_image": None}
        if getattr(content, "author", None):
            author_data["username"] = content.author.Username
            if getattr(content.author, "profile", None):
                author_data["profile_image"] = getattr(content.author.profile, "ProfileImage", None)

        response.append({
            "id": content.ContentID,
            "content_id": content.ContentID,
            "title": content.Title,
            "description": content.Description,
            "content_type": content.ContentType,
            "content_url": content.ContentURL,
            "status": content.Status,
            "is_approved": getattr(content, "IsApproved", False),
            "author_id": content.UserID,
            "author": author_data,
            "views_count": getattr(content, "ViewsCount", 0),
            "likes_count": getattr(content, "LikesCount", 0),
            "categories": [
                {"id": cat.CategoryID, "name": cat.Name}
                for cat in content.categories
            ],
            "created_at": content.CreatedAt.isoformat() if content.CreatedAt else None,
        })

    return jsonify(response), 200


# -------------------------------------------------------------------
# 2. GET SINGLE CONTENT
# -------------------------------------------------------------------
@content_bp.get("/<int:content_id>")
def get_single_content(content_id):
    item = db.session.get(Content, content_id)
    if not item:
        return jsonify({"error": "Content not found"}), 404

    author_data = {"username": None, "profile_image": None}
    if getattr(item, "author", None):
        author_data["username"] = item.author.Username
        if getattr(item.author, "profile", None):
            author_data["profile_image"] = getattr(item.author.profile, "ProfileImage", None)

    return jsonify({
        "id": item.ContentID,
        "content_id": item.ContentID,
        "title": item.Title,
        "description": item.Description,
        "type": item.ContentType,
        "content_type": item.ContentType,
        "url": item.ContentURL,
        "content_url": item.ContentURL,
        "status": item.Status,
        "is_approved": getattr(item, "IsApproved", False),
        "author_id": item.UserID,
        "author": author_data,
        "categories": [
            {"id": cat.CategoryID, "name": cat.Name}
            for cat in item.categories
        ],
        "created_at": item.CreatedAt.isoformat() if item.CreatedAt else None,
    }), 200


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

        # Handle JSON or Multipart Form-Data
        if request.is_json:
            data = request.get_json() or {}
            file = None
        else:
            data = request.form.to_dict()
            file = request.files.get("file") or request.files.get("content_url")

        title = data.get("title") or data.get("Title")
        description = data.get("description") or data.get("Description") or data.get("body") or ""
        content_type = data.get("content_type") or data.get("type") or "Article"
        category_id = data.get("category_id") or data.get("categoryId")

        if not title:
            return jsonify({"error": "Title is required"}), 400

        # File Upload Handling
        file_url = data.get("content_url") or ""
        if file:
            filename = secure_filename(file.filename)
            upload_dir = current_app.config.get("UPLOAD_FOLDER", "static/uploads")
            os.makedirs(upload_dir, exist_ok=True)
            save_path = os.path.join(upload_dir, filename)
            file.save(save_path)
            file_url = f"/static/uploads/{filename}"

        # Status Check Constraint Compliance
        req_status = str(data.get("status", "")).capitalize()
        status = req_status if req_status in ["Draft", "Published", "Archived"] else "Published"

        new_content = Content(
            Title=title,
            Description=description,
            ContentType=content_type,
            ContentURL=file_url,
            Status=status,
            UserID=user_id
        )

        if category_id:
            category = db.session.get(Category, int(category_id))
            if category:
                new_content.categories.append(category)

        db.session.add(new_content)
        db.session.commit()

        return jsonify({
            "message": "Content submitted successfully!",
            "content_id": getattr(new_content, "ContentID", getattr(new_content, "id", None)),
            "status": new_content.Status
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to submit content", "details": str(e)}), 500


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
    if item.UserID != current_user.UserID and current_user.Role != "Admin":
        return jsonify({"error": "Forbidden: Cannot edit another user's content"}), 403

    # 2. Extract Body (JSON or Form Data)
    if request.is_json:
        data = request.get_json() or {}
        file = None
    else:
        data = request.form.to_dict()
        file = request.files.get("file") or request.files.get("content_url")

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
        if req_status in ["Draft", "Published", "Archived"]:
            item.Status = req_status

    # 6. Basic Fields Update
    if "title" in data or "Title" in data:
        item.Title = data.get("title") or data.get("Title")
    if "description" in data or "Description" in data or "body" in data:
        item.Description = data.get("description") or data.get("Description") or data.get("body")

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
    if item.UserID != current_user.UserID and current_user.Role != "Admin":
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
        # ('Draft', 'Published', 'Archived')
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