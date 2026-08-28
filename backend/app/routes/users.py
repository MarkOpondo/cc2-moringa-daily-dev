from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import User, Profile
from app.utils import role_required

users_bp = Blueprint("users", __name__)

#--------------------- ADMIN ROUTES--------------
@users_bp.get("")
@jwt_required()
@role_required("admin")
def list_all_users():
    users = User.query.all()
    return jsonify([{
        "id": user.UserID,
        "username": user.Username,
        "email": user.Email,
        "role": user.Role,
        "is_active": user.IsActive
    } for user in users]),200

@users_bp.post("")   
@jwt_required()
@role_required("admin")
def admin_add_user():
    data = request.get_json() 
    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if not all ([
        data.get("username"),
         data.get("email"), 
         data.get("password")]):

        return jsonify({"error": "Username, email and password are required"}), 400
    existing = User.query.filter(
        (User.Username == data["username"]) | (User.Email ==  data["email"])
    ).first()
    
    if existing:
        return jsonify({"error": "Username or email already exists"}), 409

    new_user= User(
        Username = data["username"],
        Email=data["email"],
        Role=data.get("role", "user"),
        IsActive=True
    )    
    new_user.password_hash=data["password"]
    db.session.add(new_user)
    db.session.flush()

    db.session.add(Profile(UserID=new_user.UserID))
    db.session.commit()

    return jsonify({
        "message": "User added successfully",
        "user_id": new_user.UserID
    }), 201

@users_bp.patch("/<int:user_id>/deactivate")
@jwt_required()
@role_required("admin")
def deactivate_user(user_id):
    user= User.query.get_or_404(user_id)
    user.IsActive = not user.IsActive
    db.session.commit()
    return jsonify({
        "message": f"User '{user.Username}' has been deactivated."}),200

#--------------------------CURRENT USER ROUTES -------
@users_bp.get("/me")
@jwt_required()
def get_current_user():
    user= User.query.get(int(get_jwt_identity()))

    if not user:
        return jsonify({"error": "User not found."}),404

    return jsonify({
        "id": user.UserID,
        "username": user.Username,
        "email": user.Email,
        "role": user.Role,
        "is_active": user.IsActive
    }),200  

@users_bp.put("/me")
@jwt_required()
def update_current_user():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({
            "error": "User not found"
        }),404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required" }),400

    if "username" in data:
        # Checks for the uniqueness
        existing_username = User.query.filter(
            User.Username == data["username"],
            User.UserID != user.UserID
        ).first()

        if existing_username:
            return jsonify({"error": "Username already taken"}),200
        user.Username= data["username"]

    if "email" in data:
        existing_email= User.query.filter(
            User.Email==data["email"],
            User.UserID!= user.UserID
        ).first()
        if existing_email:
            return jsonify({
                "error": "Email already taken"
            }),409
        user.Email=data["email"]

    if "password" in data:
         user.password_hash=data["password"]

    db.session.commit()

    return jsonify({"message": "Account has been updated successfully"}),200                