from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app import db
from app.models import Profile, User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def signup():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Username, email and password are required."}), 400

    existing_user = User.query.filter(
        (User.Username == username) | (User.Email == email)
    ).first()

    if existing_user:
        return jsonify({"error": "Username or email already exists"}), 409

    new_user = User(Username=username, Email=email, Role="user", IsActive=True)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.flush()

    new_profile = Profile(UserID=new_user.UserID)
    db.session.add(new_profile)
    db.session.commit()

    return (
        jsonify({
            "message": "User created successfully.",
            "user": {
                "id": new_user.UserID,
                "username": new_user.Username,
                "email": new_user.Email,
            },
        }),
        201,
    )


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    identifier = data.get("email") or data.get("username")
    password = data.get("password")

    if not identifier or not password:
        return jsonify({"error": "Email/username and password are required"}), 400

    user = User.query.filter(
        (User.Email == identifier) | (User.Username == identifier)
    ).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email/username or password"}), 401

    if hasattr(user, "IsActive") and not user.IsActive:
        return jsonify({"error": "Account is inactive"}), 403

    access_token = create_access_token(identity=str(user.UserID))
    is_admin = getattr(user, "is_admin", False) or (
        getattr(user, "Role", "").lower() == "admin"
    )

    return (
        jsonify({
            "token": access_token,
            "access_token": access_token,  # Dual key support for Axios/Fetch clients
            "message": "Login successful",
            "user": {
                "id": user.UserID,
                "username": user.Username,
                "email": user.Email,
                "is_admin": is_admin,
            },
        }),
        200,
    )


@auth_bp.post("/logout")
def logout():
    return jsonify({"message": "Logout successful"}), 200


@auth_bp.get("/me")
@jwt_required()
def get_current_user():
    raw_identity = get_jwt_identity()
    try:
        current_user_id = int(raw_identity)
    except (ValueError, TypeError):
        current_user_id = raw_identity

    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    is_admin = getattr(user, "is_admin", False)
    if not is_admin and hasattr(user, "Role"):
        is_admin = user.Role.lower() == "admin"

    return (
        jsonify({
            "id": user.UserID,
            "username": user.Username,
            "email": user.Email,
            "role": getattr(user, "Role", "user"),
            "is_admin": is_admin,
        }),
        200,
    )