
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from app.extensions import db
from app.models import User, Profile
from app.email_service import send_password_reset_email


auth_bp = Blueprint("auth", __name__)



# PASSWORD RESET TOKEN HELPERS


def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    return serializer.dumps(
        email,
        salt="password-reset"
    )


def verify_reset_token(token):
    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    try:
        return serializer.loads(
            token,
            salt="password-reset",
            max_age=current_app.config["PASSWORD_RESET_TOKEN_MAX_AGE"]
        )

    except (SignatureExpired, BadSignature):
        return None



# REGISTER


@auth_bp.post("/register")
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
              example: ann123
            email:
              type: string
              example: ann@example.com
            password:
              type: string
              example: Password123
    responses:
      201:
        description: User created successfully
      400:
        description: Invalid input
    """
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No input data provided."
        }), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not all([username, email, password]):
        return jsonify({
            "error": "username, email, password are required"
        }), 400

    existing = User.query.filter(
        (User.Username == username) |
        (User.Email == email)
    ).first()

    if existing:
        return jsonify({
            "error": "Username or email already exists."
        }), 400

    new_user = User(
        Username=username,
        Email=email,
        Role="user",
        IsActive=True
    )

    new_user.password_hash = password

    db.session.add(new_user)
    db.session.flush()

    new_profile = Profile(
        UserID=new_user.UserID
    )

    db.session.add(new_profile)
    db.session.commit()

    return jsonify({
        "message": "User created successfully.",
        "user_id": new_user.UserID
    }), 201



# LOGIN


@auth_bp.post("/login")
def login():
    """
    Login 
    user
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: ann123
            password:
              type: string
              example: Password123
    responses:
      200:
        description: Login successful
      401:
        description: Invalid username or password
      403:
        description: Account is inactive
    """
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No input data provided."
        }), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Username and password are required"
        }), 400

    user = User.query.filter_by(
        Username=username
    ).first()

    if not user or not user.authenticate(password):
        return jsonify({
            "error": "Invalid Username or password"
        }), 401

    if not user.IsActive:
        return jsonify({
            "error": "Account is inactive. Contact the admin"
        }), 403

    access_token = create_access_token(
        identity=str(user.UserID)
    )

    return jsonify({
        "token": access_token,
        "user": {
            "id": user.UserID,
            "username": user.Username,
            "email": user.Email,
            "role": user.Role
        },
        "message": "Login successful"
    }), 200



# LOGOUT


@auth_bp.post("/logout")
def logout():
    """
    Logout user
    ---
    tags:
      - Authentication
    responses:
      200:
        description: Logout successful
    """
    return jsonify({
        "message": "Logout successful."
    }), 200



# FORGOT PASSWORD


@auth_bp.post("/forgot-password")
def forgot_password():
    """
    Request a password reset
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
          properties:
            email:
              type: string
              example: testuser01@example.com
    responses:
      200:
        description: Password reset request processed
      400:
        description: Email is required
      500:
        description: Unable to send password reset email
    """
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No input data provided."
        }), 400

    email = data.get("email")

    if not email:
        return jsonify({
            "error": "Email is required."
        }), 400

    user = User.query.filter_by(
        Email=email
    ).first()

    # Do not reveal whether an email exists in the database.
    if not user:
        return jsonify({
            "message": (
                "If an account with that email exists, "
                "password reset instructions have been sent."
            )
        }), 200

    token = generate_reset_token(user.Email)

    frontend_url = current_app.config["FRONTEND_URL"]

    reset_url = (
        f"{frontend_url}/reset-password?token={token}"
    )

    try:
        send_password_reset_email(
            user.Email,
            reset_url
        )

    except Exception:
        current_app.logger.exception(
            "Failed to send password reset email."
        )

        return jsonify({
            "error": "Unable to send password reset email."
        }), 500

    return jsonify({
        "message": (
            "If an account with that email exists, "
            "password reset instructions have been sent."
        )
    }), 200



# RESET PASSWORD


@auth_bp.post("/reset-password")
def reset_password():
    """
    Reset user password
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - token
            - password
          properties:
            token:
              type: string
              example: your-reset-token
            password:
              type: string
              example: NewPassword123!
    responses:
      200:
        description: Password reset successful
      400:
        description: Invalid input or expired token
      404:
        description: User not found
    """

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No input data provided."
        }), 400

    token = data.get("token")
    password = data.get("password")

    if not token or not password:
        return jsonify({
            "error": "Token and password are required."
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must be at least 8 characters."
        }), 400

    email = verify_reset_token(token)

    if not email:
        return jsonify({
            "error": "Invalid or expired password reset token."
        }), 400

    user = User.query.filter_by(
        Email=email
    ).first()

    if not user:
        return jsonify({
            "error": "User not found."
        }), 404

    user.password_hash = password

    db.session.commit()

    return jsonify({
        "message": (
            "Password reset successful. "
            "You can now log in with your new password."
        )
    }), 200
