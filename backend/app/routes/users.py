from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import User
from app.serializers import serialize_user


users_bp = Blueprint("users", __name__)


def _current_user():
    return db.session.get(User, int(get_jwt_identity()))


@users_bp.get("/me")
@jwt_required()
def get_current_user():
    user = _current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(serialize_user(user)), 200


@users_bp.put("/me")
@jwt_required()
def update_current_user():
    user = _current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True) or {}
    if "username" in data:
        username = str(data["username"] or "").strip()
        if not username:
            return jsonify({"error": "Username cannot be empty"}), 400
        duplicate = User.query.filter(
            User.Username == username, User.UserID != user.UserID
        ).first()
        if duplicate:
            return jsonify({"error": "Username already taken"}), 409
        user.Username = username
    if "email" in data:
        email = str(data["email"] or "").strip().lower()
        duplicate = User.query.filter(
            User.Email == email, User.UserID != user.UserID
        ).first()
        if duplicate:
            return jsonify({"error": "Email already taken"}), 409
        user.Email = email
    if "password" in data:
        password = data["password"] or ""
        if not isinstance(password, str) or len(password) < 8:
            return jsonify({"error": "Password must be at least 8 characters"}), 400
        user.password_hash = password

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 409
    return jsonify(serialize_user(user)), 200
