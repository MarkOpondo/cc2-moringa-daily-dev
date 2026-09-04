from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy.exc import IntegrityError

from app.email_service import send_password_reset_email
from app.extensions import db
from app.models import Profile, User
from app.serializers import serialize_user


auth_bp = Blueprint("auth", __name__)


def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt="password-reset")


def verify_reset_token(token):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        return serializer.loads(
            token,
            salt="password-reset",
            max_age=current_app.config["PASSWORD_RESET_TOKEN_MAX_AGE"],
        )
    except (SignatureExpired, BadSignature):
        return None


def _token_response(user):
    return {
        "token": create_access_token(identity=str(user.UserID)),
        "user": serialize_user(user),
    }


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username") or "").strip()
    email = str(data.get("email") or "").strip().lower()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"error": "username, email, and password are required"}), 400
    if not isinstance(password, str) or len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
    if "@" not in email:
        return jsonify({"error": "A valid email address is required"}), 400
    if len(username) > 150 or len(email) > 200:
        return jsonify({"error": "Username or email is too long"}), 400

    existing = User.query.filter(
        (User.Username == username) | (User.Email == email)
    ).first()
    if existing:
        return jsonify({"error": "Username or email already exists"}), 409

    user = User(Username=username, Email=email, Role="user", IsActive=True)
    user.password_hash = password
    db.session.add(user)
    db.session.flush()
    db.session.add(Profile(UserID=user.UserID))

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username or email already exists"}), 409

    return jsonify({"message": "User created successfully", **_token_response(user)}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    identifier = str(data.get("identifier") or data.get("username") or data.get("email") or "").strip()
    password = data.get("password", "")

    if not identifier or not password:
        return jsonify({"error": "Identifier and password are required"}), 400

    user = User.query.filter(
        (User.Email == identifier.lower()) | (User.Username == identifier)
    ).first()
    if not user or not user.authenticate(password):
        return jsonify({"error": "Invalid username/email or password"}), 401
    if not user.IsActive:
        return jsonify({"error": "Account is inactive"}), 403

    return jsonify({"message": "Login successful", **_token_response(user)}), 200


@auth_bp.get("/me")
@jwt_required()
def get_current_user():
    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(serialize_user(user)), 200


@auth_bp.post("/logout")
def logout():
    # Access tokens are stateless; the client removes its token on logout.
    return jsonify({"message": "Logout successful"}), 200


@auth_bp.post("/forgot-password")
def forgot_password():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email") or "").strip().lower()
    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = User.query.filter_by(Email=email).first()
    if user:
        reset_url = f"{current_app.config['FRONTEND_URL']}/reset-password?token={generate_reset_token(user.Email)}"
        try:
            send_password_reset_email(user.Email, reset_url)
        except Exception:
            # Do not reveal whether an account exists through an error status.
            current_app.logger.exception("Failed to send password reset email")

    return jsonify(
        {
            "message": "If an account with that email exists, password reset instructions have been sent."
        }
    ), 200


@auth_bp.post("/reset-password")
def reset_password():
    data = request.get_json(silent=True) or {}
    token = data.get("token")
    password = data.get("password", "")
    if not token or not password:
        return jsonify({"error": "Token and password are required"}), 400
    if not isinstance(password, str) or len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    email = verify_reset_token(token)
    user = User.query.filter_by(Email=email).first() if email else None
    if not user:
        return jsonify({"error": "Invalid or expired password reset token"}), 400

    user.password_hash = password
    db.session.commit()
    return jsonify({"message": "Password reset successful"}), 200
