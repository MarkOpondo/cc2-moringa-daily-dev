from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models import Category, Content
from app.utils import role_required


categories_bp = Blueprint("categories", __name__)


def _category_payload(category):
    published_count = Content.query.filter(
        Content.Status == "Published",
        Content.IsApproved.is_(True),
        Content.categories.any(Category.CategoryID == category.CategoryID),
    ).count()
    return {
        "id": category.CategoryID,
        "name": category.Name,
        "description": category.Description,
        "contentCount": published_count,
    }


@categories_bp.get("")
def list_categories():
    return jsonify([_category_payload(category) for category in Category.query.order_by(Category.Name).all()]), 200


@categories_bp.post("")
@jwt_required()
@role_required("admin", "tech_writer")
def create_category():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "Category name is required"}), 400
    if Category.query.filter_by(Name=name).first():
        return jsonify({"error": "Category already exists"}), 409

    category = Category(
        Name=name,
        Description=str(data.get("description") or "").strip() or None,
        CreatedBy=int(get_jwt_identity()),
    )
    db.session.add(category)
    db.session.commit()
    return jsonify(_category_payload(category)), 201


@categories_bp.patch("/<int:category_id>")
@jwt_required()
@role_required("admin", "tech_writer")
def update_category(category_id):
    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    data = request.get_json(silent=True) or {}
    if "name" in data:
        name = str(data["name"] or "").strip()
        if not name:
            return jsonify({"error": "Category name cannot be empty"}), 400
        duplicate = Category.query.filter(
            Category.Name == name, Category.CategoryID != category_id
        ).first()
        if duplicate:
            return jsonify({"error": "Category already exists"}), 409
        category.Name = name
    if "description" in data:
        category.Description = str(data["description"] or "").strip() or None

    db.session.commit()
    return jsonify(_category_payload(category)), 200


@categories_bp.delete("/<int:category_id>")
@jwt_required()
@role_required("admin")
def delete_category(category_id):
    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    if category.contents.count():
        return jsonify({"error": "Categories with content cannot be deleted"}), 409

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200
