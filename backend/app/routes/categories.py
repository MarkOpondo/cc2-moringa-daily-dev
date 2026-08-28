from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from app.extensions import db
from app.models import Category
from app.utils import role_required

categories_bp = Blueprint("categories", __name__)

#---------------------- LIST CATEGORIES --------
@categories_bp.get("")
def list_categories():
    categories = Category.query.all()
    return jsonify([{
        "id": categories.CategoryID,
        "name": categories.Name,
        "description": categories.Description
    }for category in categories]), 200

#----------------- CREATE CATEGORY ----------------
@categories_bp.post("")
@jwt_required()
@role_required("admin", "tech_writer")
def create_category():
    data = request.get_json()
    if not data:
        return jsonify({
            "error": "Request body required"
            }),400

    name= data.get("name")
    if not name:
        return jsonify({"error": "Category name is required."}),409

    # Check if category already exists
    existing_category = Category.query.filter_by(
        Name= name
    ).first()
    if existing_category:
        return jsonify({
            "error": "Category already exists."
        }),409
    new_category = Category(
        Name=name,
        Description=data.get("description"),
        CreatedBy=int(get_jwt_identity())
        )
    db.session.add(new_category)
    db.session.commit()

    return jsonify({
        "id": new_category.CategoryID,
         "name": new_category.Name}), 201

#--------------------- UPDATE CATEGORY ----------------
@categories_bp.put("/<int:category_id>")
@jwt_required()
@role_required("admin", "tech_writer")
def update_category(category_id):
    category = Category.query.get_or_404(category_id)

    data = request.get_json()
    if not data:
        return jsonify({
            "error": "Request body is required"
        }),400
    if "name" in data:
        existing_category=Category.query.filter(
            Category.Name == data["name"],
            Category.CategoryID != category.CategoryID
        ).first()

        if existing_category:
            return jsonify({
                "error": "Category already exists"
             }) ,409       

    category.Name = data["name"]
    if "description" in data:
        category.Description = data["description"]
    db.session.commit()
    
    return jsonify({
        "id": category.CategoryID,
        "name": category.Name,
        "description": category.Description
    }),200

#------------------ DELETE CATEGORY--------------------
@categories_bp.delete("/<int:category_id>")
@jwt_required()
@role_required("admin")
def delete_category(category_id):
    category= Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted"}), 200


