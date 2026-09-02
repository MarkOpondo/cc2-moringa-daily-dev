from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Content, User, Category, Subscription, Notification
from app.utils import role_required

content_bp = Blueprint("content", __name__)


# ----------------------------- NOTIFY SUBSCRIBERS -----------------------------
def _notify_subscribers(content_item):
    """Send notifications to users subscribed to this content's categories."""
    notifications = []
    for category in content_item.categories:
        subscriptions = Subscription.query.filter_by(CategoryID=category.CategoryID).all()
        for sub in subscriptions:
            if sub.UserID != content_item.UserID:
                notifications.append(
                    Notification(
                        UserID=sub.UserID,
                        ContentID=content_item.ContentID,
                        Message=f"New content in your feed: '{content_item.Title}'"
                    )
                )

    if notifications:
        db.session.add_all(notifications)
        db.session.commit()


# ------------------------- PUBLIC CONTENT ROUTES -------------------------

# GET LIST OF CONTENT
@content_bp.get("")
def list_content():
    category_id = request.args.get("category_id", type=int)
    status = request.args.get("status")
    content_type = request.args.get("type")

    query = Content.query

    # Filter by category through the many-to-many relationship
    if category_id:
        query = query.filter(Content.categories.any(Category.CategoryID == category_id))

    if content_type:
        query = query.filter_by(ContentType=content_type)

    if status:
        query = query.filter_by(Status=status)

    items = query.order_by(Content.CreatedAt.desc()).all()

    return jsonify([
        {
            "id": content.ContentID,
            "title": content.Title,
            "description": content.Description,
            "type": content.ContentType,
            "url": content.ContentURL,
            "status": content.Status,
            "author_id": content.UserID,
            "categories": [
                {
                    "id": cat.CategoryID,
                    "name": cat.Name
                } for cat in content.categories
            ],
            "created_at": content.CreatedAt.isoformat() if content.CreatedAt else None
        } for content in items
    ]), 200


# GET SINGLE CONTENT ITEM
@content_bp.get("/<int:content_id>")
def get_single_content(content_id):
    item = Content.query.get_or_404(content_id)

    return jsonify({
        "id": item.ContentID,
        "title": item.Title,
        "description": item.Description,
        "type": item.ContentType,
        "url": item.ContentURL,
        "status": item.Status,
        "author_id": item.UserID,
        "categories": [
            {
                "id": category.CategoryID,
                "name": category.Name
            } for category in item.categories
        ],
        "created_at": item.CreatedAt.isoformat() if item.CreatedAt else None
    }), 200


# --------------------------- CREATE CONTENT ---------------------------
@content_bp.post("")
@jwt_required()
@role_required("tech_writer", "user")
def create_content():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    required = ["title", "type", "category_id"]

    if not all(data.get(field) for field in required):
        return jsonify({"error": "title, type, and category_id are required."}), 400

    category = Category.query.get(data["category_id"])
    if not category:
        return jsonify({"error": "Category not found"}), 404

    # Auto-approve for admin/tech_writer; default to pending for regular users
    status = "Approved" if user.Role in ["admin", "tech_writer"] else "pending"
    is_approved = True if status == "Approved" else False

    new_content = Content(
        UserID=user_id,
        Title=data["title"],
        Description=data.get("description"),
        ContentType=data["type"],
        ContentURL=data.get("url"),
        Status=status,
        IsApproved=is_approved
    )

    # Add category via relationship
    new_content.categories.append(category)

    db.session.add(new_content)
    db.session.commit()

    return jsonify({
        "id": new_content.ContentID,
        "message": "Content submitted successfully"
    }), 201


# ------------------------------ EDIT CONTENT ------------------------------
@content_bp.put("/<int:content_id>")
@jwt_required()
@role_required("tech_writer", "admin")
def edit_content(content_id):
    item = Content.query.get_or_404(content_id)
    current_user = User.query.get(int(get_jwt_identity()))

    if not current_user:
        return jsonify({"error": "User not found"}), 404

    if item.UserID != current_user.UserID and current_user.Role != "admin":
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    item.Title = data.get("title", item.Title)
    item.Description = data.get("description", item.Description)
    item.ContentURL = data.get("url", item.ContentURL)
    item.ContentType = data.get("type", item.ContentType)

    # Update category if provided
    if "category_id" in data:
        category = Category.query.get(data["category_id"])
        if not category:
            return jsonify({"error": "Category not found"}), 404
        item.categories = [category]

    db.session.commit()
    return jsonify({"message": "Content updated."}), 200


# -------------------------- DELETE CONTENT --------------------------
@content_bp.delete("/<int:content_id>")
@jwt_required()
def delete_content(content_id):
    item = Content.query.get_or_404(content_id)

    current_user = User.query.get(int(get_jwt_identity()))
    if not current_user:
        return jsonify({"error": "User not found"}), 404

    if item.UserID != current_user.UserID and current_user.Role != "admin":
        return jsonify({"error": "Forbidden."}), 403

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Content deleted"}), 200


# ------------------------ APPROVE CONTENT -----------------
@content_bp.patch("/<int:content_id>/approve")
@jwt_required()
@role_required("admin", "tech_writer")
def approve_content(content_id):
    item = Content.query.get_or_404(content_id)

    item.Status = "Published"
    item.IsApproved = True

    db.session.commit()

    _notify_subscribers(item)
    return jsonify({"message": "Content approved"}), 200


# --------------------------------- FLAG CONTENT -----------------
@content_bp.patch("/<int:content_id>/flag")
@jwt_required()
@role_required("admin", "tech_writer")
def flag_content(content_id):
    item = Content.query.get_or_404(content_id)

    item.IsApproved = False
    item.Status = "Flagged"
    db.session.commit()

    return jsonify({"message": "Content flagged."}), 200